import React from 'react'
import qs from 'query-string'

import './index.css'
import logo from './logo.png'
import background from './header.png'

export default function Header(props) {
  const userInfo = qs.parse(window.location.search)
  return (
    <div>
      <div className='header-container'>
        <img src={background} alt="background不见了" className='background' />
        <div className='foreground'>
          <div className='line1'>
            <img src={logo} alt="logo不见了" className='logo' />
            <span className='text1'>校园通行证</span>
          </div>
          <div className='line2'>
            {`${userInfo.name} (学生)`}
          </div>
          <div className='line3'>
            {`${userInfo.major}`}
          </div>
        </div>
      </div>
    </div>
  )
}
