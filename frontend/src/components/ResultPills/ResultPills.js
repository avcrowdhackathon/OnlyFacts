import React from 'react'
import Pill from './Pill';
export default function ResultPills({ results }) {
    delete results.subjectivity;
    const names = Object.keys(results);
    const percentages = Object.values(results)
    return (
        <div className={'pills-container'}>
            { names.map((name, index) => <Pill name={name} percent={percentages[index]} />)}
        </div>
    )
}
