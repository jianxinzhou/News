import React from 'react';
import PropTypes from 'prop-types';
import Auth from '../Auth/Auth';

import LoginForm from './LoginForm';

class LoginPage extends React.Component {
    constructor(props, context) {
        super(props, context);

        // 设置component的初始状态
        this.state = {
            errors: {},
            user: {
                email: '',
                password: ''
            }
        };

        this.processForm = this.processForm.bind(this);
        this.changeUser = this.changeUser.bind(this);
    }

    processForm(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;

        // 向服务端发起post request，验证登录数据
        fetch('http://localhost:3000/auth/login', {
            method: 'POST',
            cache: false,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }).then(response => {
            if (response.status === 200) {
                this.setState({
                    // errors中可能存着上次登录失败的信息，登录成功，则清空errors
                    errors: {}
                });

                response.json().then(function(json) {
                    console.log(json);
                    // 登录成功后，把从server拿到的token和email存储在本地
                    Auth.authenticateUser(json.token, email);
                    // 登录成功，重定向到根目录
                    this.context.router.replace('/');
                }.bind(this));
            } else {
                console.log('Login failed');
                response.json().then(function(json) {
                    // error message后端会写好
                    const errors = json.errors ? json.errors : {};
                    errors.summary = json.message;
                    // 登录失败，errors需要setState一把
                    this.setState({errors});
                }.bind(this));
            }
        });
    }

    // 在LoginForm中，对用户名或密码输入框做任何改动，
    // 例如添加一个字符，都会触发changeUser函数，
    // 将用户名或者密码更新到LoginPage的user state中，
    // 这样，当点击submit触发processForm函数时，可以在前端拿到最新的用户名和密码的输入信息，
    // 从而向服务端发起Post请求，验证登录信息
    changeUser(event) {
        const field = event.target.name;
        const user = this.state.user;
        user[field] = event.target.value;
        // user['email'] = '123@123.com'
        // user['password'] = '12345678'

        this.setState({ user });
    }

    // render并没有自己UI的部分，完全调用的LoginForm，
    // 当前的调用关系是LoginPage调用LoginForm，
    // LoginPage可以通过propeties的方式向LoginForm传递信息，例如这里的errors、uesr，
    // 那如何从LoginForm往上向LoginPage传递信息呢（例如用户在密码文本框输入的内容）？
    // 通过LoginPage向LoginForm传递的处理函数，例如此处的onSubmit，onChange，
    // 当在LoginForm中填写密码时，会触发onChange函数，改变LoginPage中state的状态
    render() {
        return (
            <LoginForm
            onSubmit={this.processForm}
            onChange={this.changeUser}
            errors={this.state.errors}
            user={this.state.user}
            />
        );
    }
}

// To make react-router work
LoginPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default LoginPage;
