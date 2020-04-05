import React from 'react';
import './styles.scss'

export default function Pill({name, percent}) {
    const colorPalette = ['#0064b7', '#64dd17', '#ffd600', '#d50000']
    let color;
    switch(true) {
        case (percent === 0):
            color = '#0075d6';
            break;
        case (percent < 0.4):
            color = colorPalette[0]
            break;
        case (percent < 0.9):
            color = colorPalette[1]
            break;
        case (percent < 1.4):
            color = colorPalette[2]
            break;
        case (percent >= 1.5):
            color = colorPalette[3]
            break;
    } 
    return (
        <div className={'pill'} style={{ background: color }}>
            { name }: { percent }
        </div>
    )
}
