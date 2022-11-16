import React, { Component } from 'react'

import './index.css'
import Part2v1 from './Part2v1/index'
import Part2v2 from './Part2v2/index'

export default class Part2 extends Component {
  render() {
    return (
      <div className='Part2-container'>
        <Part2v1/>
        <Part2v2/>
      </div>
    )
  }
}
