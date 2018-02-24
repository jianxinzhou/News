// helper class to manipulate localStorage
class Auth {
    /**
    * Authenticate a user. Save a token string in Local Storage
    *
    * @param {string} token
    * @param {string} email
    */
    static authenticateUser(token, email) {
        // 把收到的token和email（用户名）存到localStorage中
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);
    }

    /**
    * Check if a user is authenticated - check if a token is saved in Local Storage
    * 很容易骗过前端，可以伪造token（极端一点临时打开console随便写一个token）
    * 但是不能从server拿到数据（后端会验证token）
    * @returns {boolean}
    */
    static isUserAuthenticated() {
        return localStorage.getItem('token') !== null;
    }

    /**
    * Deauthenticate a user. Remove token and email from Local Storage.
    *
    */
    static deauthenticateUser() {
        // 用户logout时，清掉token和用户名
        localStorage.removeItem('token');
        localStorage.removeItem('email');
    }

    /**
    * Get a token value.
    *
    * @returns {string}
    */
    static getToken() {
        return localStorage.getItem('token');
    }

    /**
    * Get email.
    *
    * @returns {string}
    */
    static getEmail() {
        return localStorage.getItem('email');
    }
}

export default Auth;
