import React from 'react';
import './App.scss';

import NewsRow from './components/NewsRow'

import articles from './components/articles';

function App() {
  return (
    <div className="App">
      <div className={'main-container'}>
        {articles.map(article => 
          (
            <div className={'article-wrapper'}>
              <NewsRow
                title={article.title}
                results={article.results}
                articleContent={article.content}
                objectiveness={article.results.subjectivity}
              />
            </div>
          ))}
      </div>
    </div>
  );
}

export default App;
