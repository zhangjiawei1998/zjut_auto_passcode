import React, { Component } from 'react'
import './index.css'
import icon from './icon.png'

export default class Part2v2 extends Component {
  render() {
    return (
      // 中间右边
      <div className='Part2_2-container'>
        <div className='Part2_2_text'>
          <div className='text1'>疫情重点地区核验</div>
          <div className='text2'>未查到您的行程记录。</div>
        </div>
        <div className='Part2_2_icon'>
          <img src={icon} alt="重新校验icon" className='icon'/>
        </div>
      </div>
      
    )
  }
}
