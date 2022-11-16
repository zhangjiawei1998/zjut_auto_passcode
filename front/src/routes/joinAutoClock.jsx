import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import './index.css'

function throttle(fun, delay=500) {
  let timer = null
  let flag = true

  return function(){
    if(flag == false){
      window.alert('请勿频繁提交')
      return
    }
    flag = false

    if(timer)
      window.clearTimeout(timer)
      
    timer = setTimeout(() => {
      flag = true
      fun.apply(this, arguments)
    }, delay) 
  }
}

export default function JoinAutoClock(props) {
  // 按钮是否能点击
  const [btnFlag, setBtnFlag] = useState(false)
  // 自动打卡信息
  const [name, setName] = useState('')
  const [id, setId] = useState('')
  const [mobile, setMobile] = useState('')
  const [grade, setGrade] = useState('2021')
  const [sex, setSex] = useState('1')
  const [company, setCompany] = useState('信息工程学院')
  const [emLinkPerson, setEmLinkPerson] = useState('')
  const [emLinkMobile, setEmLinkMobile] = useState('')
  const [auditName, setAuditName] = useState('')
  
  // 是否停止自动打卡
  const [stop, setStop] = useState(false)
  const [stopId, setStopId] = useState('')

  // 补打卡id
  const [appealId, setAppealId] = useState('')

  function submit() {
    
    const stuInfo = {
      name: name,
      id: id,
      mobile: mobile,
      grade: grade,
      sex: sex,
      company: company,
      emLinkPerson: emLinkPerson,
      emLinkMobile: emLinkMobile,
      auditName: auditName,
      auditId: '',
    }
    // 简单的验证
    const reg = new RegExp("[\\u4E00-\\u9FFF]+")
    const reg1 = new RegExp("[a-zA-Z]+")
    if(!reg.test(stuInfo.name) || reg1.test(stuInfo.name)){
      window.alert('姓名应为汉字')
      return
    }
    if(!/\d{10}/.test(stuInfo.id) || stuInfo.id.length !== 10){
      window.alert('学号应为10位数字')
      return
    }
    if(!/\d{11}/.test(stuInfo.mobile) || stuInfo.mobile.length !== 11){
      window.alert('手机号应为11位数字')
      return
    }
    if(!reg.test(stuInfo.emLinkPerson) || reg1.test(stuInfo.emLinkPerson)){
      window.alert('紧急联系人姓名应为汉字')
      return
    }
    if(!/\d{11}/.test(stuInfo.emLinkMobile) || stuInfo.emLinkMobile.length !== 11){
      window.alert('紧急联系人电话应为11位数字')
      return
    }
    if(!reg.test(stuInfo.auditName) || reg1.test(stuInfo.auditName)){
      window.alert('辅导员姓名应为汉字')
      return
    }
    setBtnFlag(true)
    axios({
      url: 'https://notzjw.top/autoAppeal/join',
      method: 'post',
      data: stuInfo,
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
        setBtnFlag(true)
      },
      reason => {
        window.alert(`加入失败, 原因: ${reason.message}`)
        setBtnFlag(true)
      }
    )

  }

  function stopClock() {
    // 简单的验证
    if( !/\d{10}/.test(stopId) || stopId.length !== 10){
      window.alert('学号应该为10位数字')
      return
    }
    setBtnFlag(true)
    axios({
      url: 'https://notzjw.top/autoAppeal/stopClock',
      method: 'post',
      data: { id: stopId },
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
        setBtnFlag(false)
      },
      reason => {
        window.alert(`停止打卡失败, 原因: ${reason.message}`)
        setBtnFlag(false)
      }
    )
  }

  function search() {
    if( !/\d{10}/.test(stopId) || stopId.length !== 10){
      window.alert('学号应该为10位数字')
      return
    }
    setBtnFlag(true)
    axios({
      url: 'https://notzjw.top/autoAppeal/search',
      method: 'post',
      data: { id: stopId },
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
        setBtnFlag(false)
      },
      reason => {
        window.alert(`查询信息失败, 原因: ${reason.message}`)
        setBtnFlag(false)
      }
    )
  }

  return (
    <div className="App-container">
      <h className='title'>加入自动打卡大家庭吧</h>
      <form>
        <fieldset className='fieldset'>
          <span className='field'>姓&emsp;名: </span>
          <input className='input' className='input' type="text" onInput={(e) => setName(e.target.value)} />
          
          <span className='field'>学&emsp;号: </span>
          <input className='input' type="number" onInput={(e) => setId(e.target.value)} />
      
          <span className='field'>手机号: </span>
          <input className='input' type="tel" onInput={(e) => setMobile(e.target.value)} />
          
          <span className='field'>年&emsp;级: </span>
          <select className='input' defaultValue={'2021'} onChange={(e) => setGrade(e.target.value)} >
            <option value="2019">2019级</option>
            <option value="2020">2020级</option>
            <option value="2021">2021级</option>
            <option value="2022">2022级</option>
          </select>
          
          <span className='field'>性&emsp;别: </span>
          <select className='input' defaultValue={'1'} onChange={(e) => setSex(e.target.value)} >
            <option value="1">boy</option>
            <option value="0">girl</option>
          </select>
          
          <span className='field'>学&emsp;院: </span>
          <input className='input' type="text" defaultValue={'信息工程学院'} onInput={(e) => setCompany(e.target.value)} />
          
          <span className='field'>紧急联系人: </span>
          <input className='input' type="text" onInput={(e) => setEmLinkPerson(e.target.value)} />
          
          <span className='field'>紧急联系人电话: </span>
          <input className='input' type="tel" onInput={(e) => setEmLinkMobile(e.target.value)} />
          

          <span className='field'>辅导员: </span>
          <input className='input' type="text" onInput={(e) => setAuditName(e.target.value)} />
          

        </fieldset>
      </form>
      <button className='submit-btn btn' disabled={btnFlag} onClick={throttle(submit, 500)}>提交</button>

      {/* <div className='divid-line'></div> */}
      <div className='whtie-block'></div>

      <h className='title'>停止/启动自动打卡 || 查询信息</h>
      <fieldset  className='fieldset'>
        <span className='field'>学&emsp;号: </span>
        <input className='input' type="text" onInput={(e) => setStopId(e.target.value)}/>
      </fieldset>
      <div className='btn-group'>
        <button className='stop-btn btn' disabled={btnFlag} onClick={throttle(stopClock, 500)}>停止/启动</button>
        <button className='search-btn btn' disabled={btnFlag} onClick={throttle(search, 500)}>查询</button>
      </div>
      
      <div className='whtie-block'></div>
{/* 
      <fieldset className='fieldset'>
        <legend>补打卡来这里！</legend>
        <span className='field'>学&emsp;号: </span>
        <input className='input' type="text" onInput={(e) => setAppealId(e.target.value)}/>
      </fieldset>
      <button className='appeal-btn btn' onClick={throttle(appeal, 2000)}>提交</button> */}
    
    </div>
  )
}