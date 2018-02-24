import React from 'react';
import PropTypes from 'prop-types';
import SignUpForm from './SignUpForm';


class SignUpPage extends React.Component {
    constructor(props, context) {
        super(props, context);

        // 设置component初始状态
        this.state = {
            // errors: {summary: 'summary error', email: 'email error', password: 'password error'}
            errors: {},
            user: {
                email: '',
                password: '',
                confirm_password: ''
            }
        };

        this.processForm = this.processForm.bind(this);
        this.changeUser = this.changeUser.bind(this);
    }

    // Pre-submission.
    processForm(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;
        const confirm_password = this.state.user.confirm_password;

        if (password !== confirm_password) {
            return;
        }

        // Post signup data.
        fetch('http://localhost:3000/auth/signup', {
            method: 'POST',
            cache: false,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }).then(response => {
            if (response.status === 200) {
                this.setState({
                    errors: {}
                });

                // change the current URL to /login
                this.context.router.replace('/login');
            } else {
                response.json().then(function(json) {
                    console.log(json);
                    const errors = json.errors ? json.errors : {};
                    errors.summary = json.message;
                    this.setState({errors});
                }.bind(this));
            }
        });
    }

    changeUser(event) {
        const field = event.target.name;
        const user = this.state.user;
        user[field] = event.target.value;

        this.setState({user});

        if (this.state.user.password !== this.state.user.confirm_password) {
            const errors = this.state.errors;
            errors.password = "Password and Confirm Password don't match.";
            this.setState({errors});
        } else {
            const errors = this.state.errors;
            errors.password = '';
            this.setState({errors});
        }
    }

    render() {
        return (
            <SignUpForm
            onSubmit={this.processForm}
            onChange={this.changeUser}
            errors={this.state.errors}
            user={this.state.user}
            />
        );
    }
}

// To make react-router work
SignUpPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default SignUpPage;
