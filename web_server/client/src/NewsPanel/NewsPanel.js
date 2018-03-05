import './NewsPanel.css';
import Auth from '../Auth/Auth'
import React from 'react';
import _ from 'lodash';

import NewsCard from '../NewsCard/NewsCard';

class NewsPanel extends React.Component {
    // 在建立component的时候会被调用
    constructor() {
        super();
        // 这个state是自己内部想keep的一个内部量
        // newspanel里到底有多少个news（newscard）
        // this.state = {news: null};
        this.state = {
            news: null,
            pageNum: 1,
            loadedAll: false,
        }
        // 对handleScroll以后的调用是以callback的方式
        // 因此需要绑定this，这样才能调用loadMoreNews等其他方法
        this.handleScroll = this.handleScroll.bind(this);
    }

    // constructor以后会立刻执行
    componentDidMount() {
        this.loadMoreNews();
        // 去抖动，减少触发频率，1秒内的所有请求都认为是一个请求
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
        // 绑定事件
        window.addEventListener("scroll", this.handleScroll);
    }


    handleScroll() {
        // scrollY是文档在垂直方向已滚动的像素值
        // 用或操作，是考虑到浏览器的兼容性，取第一个不为空的值
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        // window.innerHeight - 浏览器窗口的内部高度
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
            this.loadMoreNews();
        }
    }


    // 从后端去拿新闻，通过rest api的方式
    loadMoreNews() {
        if (this.state.loadedAll === true) {
            return;
        }

        console.log(this.state.pageNum);

        let url = 'http://localhost:3000/news/userId/' + Auth.getEmail()
            + '/pageNum/' + this.state.pageNum;

        let request = new Request(encodeURI(url), {
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });

        fetch(request)
            .then(res => res.json()) //收到response后转成json格式
            .then((news) => {
                if (!news || news.length === 0) {
                    this.setState({
                        loadedAll: true
                    })
                }

                this.setState({
                    // 左边的news是constructor中定义的news
                    // 如果原先的news不为空，request拿到的news贴在原来news的后面，相当于append操作
                    // 如果原先的news为空，则用request拿到的news
                    news: this.state.news ? this.state.news.concat(news) : news,
                    pageNum: this.state.pageNum + 1,
                })
            });
    }


    renderNews() {
        /*
        有多少条新闻，就会产生多少段
        <a className='list-group-item' href='#'>
            <NewsCard news={news} />
        </a>
        一次，得到一个list——newsCardList
        */
        let newsCardList = this.state.news.map(function(news) {
            return (
                <a className='list-group-item'>
                    <NewsCard news={news} />
                </a>
            );
        });

        return (
            <div className='container-fluid'>
                <div className='list-group'>
                    {newsCardList}
                </div>
            </div>
        );
    }

    // react真正的render函数
    render() {
        if (this.state.news) {
            return (
                <div>
                    {this.renderNews()}
                </div>
            );
        } else {
            return (
                <div>
                    Loading...
                </div>
            );
        }
    }

}

export default NewsPanel;
