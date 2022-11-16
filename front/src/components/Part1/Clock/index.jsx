import React, { Component } from 'react'
import './index.css'

export default class Clock extends Component {

  constructor(){
    super()
    this.manage = React.createRef()
    this.state = {
      date: new Date(),
      clockColor:["#e06666","#e69138","#f1c232","#6aa84f","#9fc5e8","#3d85c6","#8e7cc3"]
    }
  }
  
  componentDidMount(){
    this.timeID = setInterval(
      ()=> this.tick(),
      1000
    )
    var day = this.state.date.getDay()
    this.manage.current.style.color = this.state.clockColor[day]
  }
  
  componentWillUnmount = ()=>{
    clearInterval(this.timeID)
  }

  tick = ()=>{
    this.setState({
      date: new Date()
    })
  }

  getTime = ()=>{
    var date = this.state.date , currentTime = ''
    if(date.getMonth() < 9)
      currentTime += '0'
    currentTime += date.getMonth() + 1 + '-'
    if(date.getDate() < 9)
      currentTime += '0'
    currentTime += date.getDate() + ' '
    
    if(date.getHours() < 10)
      currentTime += '0'
    currentTime += date.getHours() + ':'
    
    if(date.getMinutes() < 10)
      currentTime += '0'
    currentTime += date.getMinutes() + ':'

    if(date.getSeconds() < 10)
      currentTime += '0'
    currentTime += date.getSeconds()
    
    return currentTime
  }

  render() {
    return (
      <div className='clock' ref={this.manage}>
        {this.getTime()}
      </div>
    )
  }
}
