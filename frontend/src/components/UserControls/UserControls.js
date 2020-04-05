import React from 'react'
import './styles.scss'
export default function UserControls({judgementFunction}) {
    const handleClick = judgement => judgementFunction(judgement)
    return (
        <div>
            <button onClick={() => handleClick(true)} className={'user-control-btn agree'}>{'Ακριβές'}</button>
            <button onClick={() => handleClick(false)} className={'user-control-btn disagree'}>{'Ανακριβές'}</button>
        </div>
    )
}
