import React, { useState } from 'react';
import UserControls from '../UserControls';
import ResultPills from '../ResultPills';
import './styles.scss';

export default function NewsRow({ title, articleContent, results, objectiveness }) {
    const [ isTrustWorthy, setTrust ] = useState('');
    const judgeRow = judgement => setTrust(judgement)
    const backgroundColor = isTrustWorthy ? {background: "#1faa00"} : {background: '#a30000'}
    return (
        <div className={'news-row'} >
            <div className={'overlay'} style={isTrustWorthy !== '' ? backgroundColor: {}} />
            <div className={'title'}>
                <div>{title}</div>
                <ResultPills results={results} />
            </div>
            <div className={'content'}>
                <article className='article-content'>{articleContent}</article>
                <section className={'objectiveness-level'}>Αντικ/τητα: { objectiveness }</section>
                <UserControls judgementFunction={judgeRow}/>
            </div>
        </div>
    )
}
