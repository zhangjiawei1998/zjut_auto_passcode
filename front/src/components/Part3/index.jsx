import React, { Component } from 'react'
import './index.css'
import bottom from './bottom.png'

export default class Part3 extends Component {
  render() {
    return (
      <div className='Part3-container'>
        <img src={bottom} alt="bottom不见了" className='bottomImg'/>
      </div>
    )
  }
}
