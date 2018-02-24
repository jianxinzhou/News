import Base from './Base/Base';
import App from './App/App';
import LoginPage from './Login/LoginPage';
import SignUpPage from './SignUp/SignUpPage';
import Auth from './Auth/Auth';

// 使用configuration的方式来配置routes
const routes = {
    // base component(wrapper for the whole application).
    // 原始的component是Base（Base带一个导航栏，下面是children）
    component: Base,
    // Base中的children参数是固定用法，childRoutes给children填充component，
    // 是react-router的固定用法，
    // 对children需要动态决定render哪一个
    childRoutes: [
        {
            // 访问根目录的话，需要判断用户是否已登录，
            // 如果登录了，进到App，可以正常看到新闻，
            // 否则转到LoginPage
            path:'/',
            getComponent: (location, callback) => {
                if(Auth.isUserAuthenticated()) {
                    callback(null, App);
                } else {
                    callback(null, LoginPage);
                }
            }
        },
        {
            path: '/login',
            component: LoginPage
        },
        {
            path: '/signup',
            component: SignUpPage
        },
        {
            path: '/logout',
            onEnter: (nextState, replace) => {
                // 把localstorage中的token删掉
                Auth.deauthenticateUser();
                // 接着重定向到首页，由于localstorage中的token已经被删掉，
                // 因此Auth.isUserAuthenticated()为False，进入到LoginPage
                replace('/login');
            }
        }
    ]
};

export default routes;
