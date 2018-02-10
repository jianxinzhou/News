import './NewsPanel.css';

import React from 'react';

import NewsCard from '../NewsCard/NewsCard';


class NewsPanel extends React.Component {
    // 在建立component的时候会被调用
    constructor() {
        super();
        // 这个state是自己内部想keep的一个内部量
        // newspanel里到底有多少个news（newscard）
        this.state = {news: null};
    }

    // constructor以后会立刻执行
    componentDidMount() {
        this.loadMoreNews();
    }

    // 暂时对news进行硬编码，后面会改成从后端去拿新闻，通过rest api的方式
    loadMoreNews(e) {
        this.setState({
            news: [
                {'url':'http://us.cnn.com/2017/02/15/politics/andrew-puzder-failed-nomination/index.html',
                 'title':"Inside Andrew Puzder's failed nomination",
                 'description':"In the end, Andrew Puzder had too much baggage -- both personal and professional -- to be confirmed as President Donald Trump's Cabinet.",
                 'source':'cnn',
                 'urlToImage':'http://i2.cdn.cnn.com/cnnnext/dam/assets/170215162504-puzder-trump-file-super-tease.jpg',
                 'digest':"3RjuEomJo26O1syZbU7OHA==\n",
                 'reason':"Recommend"
                },
                {'title': 'Zero Motorcycles CTO Abe Askenazi on the future of two-wheeled EVs',
                 'description': "Electric cars and buses have already begun to take over the world, but the motorcycle industry has been much slower to put out all-electric and hybrid models...",
                 'url': "https://techcrunch.com/2017/03/23/zero-motorcycles-cto-abe-askenazi-on-the-future-of-two-wheeled-evs/",
                 'urlToImage': "https://tctechcrunch2011.files.wordpress.com/2017/03/screen-shot-2017-03-23-at-14-04-01.png?w=764&h=400&crop=1",
                 'source': 'techcrunch',
                 'digest':"3RjuEomJo26O1syZbUdOHA==\n",
                 'time':"Today",
                 'reason':"Hot"
                }
            ]
        })
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
