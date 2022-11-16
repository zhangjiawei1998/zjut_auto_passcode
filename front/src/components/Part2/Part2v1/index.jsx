import React, { Component } from 'react'
import './index.css'

export default class Part2v1 extends Component {

  componentDidMount = ()=>{
    
  }

  getNucleicSampleTime = ()=>{
    var date = new Date() , sampleTime = ''
    console.log(date)
    var randomDay = Math.ceil(Math.random()*2)
    var randomHour = Math.floor(Math.random()*9)

    if(date.getMonth() < 9)
      sampleTime += '0'
    sampleTime += date.getMonth() + 1 + '.'

    if((date.getDate() - randomDay)<0)
      sampleTime += '01'
    else{
      if(date.getDate() < 9)
        sampleTime += '0'
      sampleTime += date.getDate() - randomDay + ' '
    }
     
    
    if(date.getHours() < 10){
      sampleTime += '0'
      sampleTime += date.getHours() + ':'
    }
    else
      sampleTime += date.getHours()-randomHour + ':'
    
    
    if(date.getMinutes() < 10)
      sampleTime += '0'
    sampleTime += date.getMinutes() + ':'

    if(date.getSeconds() < 10)
      sampleTime += '0'
    sampleTime += date.getSeconds()
    
    return sampleTime
  }

  render() {
    return (
      <div className='Part2_1'>
        <div className='line2_1_1'>核酸检测 </div>
        <div className='line2_1_2'>{this.getNucleicSampleTime()}</div>
        <div className='line2_1_3'>阴性 72h内</div>
      </div>
    )
  }
}
