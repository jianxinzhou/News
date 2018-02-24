const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const UserSchema = new mongoose.Schema(
    {
        email: {
            type: String,
            index: {unique: true}
        },
        password: String,
    }
)

UserSchema.methods.comparePassword =
    function comparePassword(password, callback) {
        // bcrypt功能：密码hash+salt
        // this.password是数据库中存储的password
        bcrypt.compare(password, this.password, callback);
    }

// 用户注册时需要将用户信息存储到数据库，以下是在save之前的预操作
UserSchema.pre(
    'save',
    function saveHook(next) {
        const user = this

        // processed futher only if the password is modified or the user is new.
        if (!user.isModified('password'))
            return next()

        return bcrypt.genSalt(
            (saltError, salt) => {
                if (saltError)
                    return next(saltError)

                return bcrypt.hash(
                    user.password,
                    salt,
                    (hashError, hash) => {
                        if (hashError)
                            return next(hashError)

                        // replace a password string with hashed value
                        user.password = hash;
                        return next();
                    }
                )
            }
        )
    }
)

module.exports = mongoose.model('User', UserSchema);
