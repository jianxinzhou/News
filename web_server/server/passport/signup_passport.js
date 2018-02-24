const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;

module.exports = new PassportLocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    session: false,
    passReqToCallback: true
}, (req, email, password, done) => {
    const userData = {
        email: email.trim(),
        password: password.trim(),
    };

    const newUser = new User(userData);
    newUser.save((err) => {
        // 如果存在同名用户，会抛出错误，原因在于models/user.js中，设定了用户名为unique
        console.log('Save new user!');
        if (err) {
            return done(err);
        }

        return done(null);
    });
});
