import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import './index.css'

// 节流函数
function throttle(fun, delay=200) {
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
// 自动获取当前位置
const getCurrentPosition = (setCurrentLocation) => {
  window.AMap.plugin('AMap.Geolocation', ()=>{
    const Geolocation = new window.AMap.Geolocation()
    Geolocation.getCurrentPosition((status, result) => {
      if(status === 'complete'){
        const province = result.addressComponent.province
        const city = result.addressComponent.city
        const district = result.addressComponent.district
        const position = province + city + district
        setCurrentLocation(position)
        window.alert(`自动获取当前位置成功\n${position}`, )
      }else{
        window.alert('自动获取当前位置失败, 请手动输入')
      }
    })
  })
  /* 获取省 市 区 数据列表 */
  // window.AMap.plugin('AMap.DistrictSearch', ()=>{
  //   const districtSearch = new window.AMap.DistrictSearch({
  //     // 关键字对应的行政区级别，country表示国家
  //     level: 'country', // 可选值： country：国家 province：省/直辖市 city：市 district：区/县 biz_area：商圈
  //     //  显示下级行政区级数，1表示返回下一级行政区
  //     subdistrict: 3
  //   })
  //   districtSearch.search('中国', (status, result) => {
  //     console.log(status, result)
  //   })
  // })
}

export default function JoinAutoClock(props) {
  // 自动打卡信息
  const [name, setName] = useState('')
  const [id, setId] = useState('')
  const [mobile, setMobile] = useState('')
  const [grade, setGrade] = useState('2021')
  const [sex, setSex] = useState('1')
  const [company, setCompany] = useState('信息工程学院')
  const [currentLocation, setCurrentLocation] = useState('')
  const [whetherInSchool, setWhetherInSchool] = useState('3')
  const [emLinkPerson, setEmLinkPerson] = useState('')
  const [emLinkMobile, setEmLinkMobile] = useState('')
  const [auditName, setAuditName] = useState('')
  
  // 是否停止自动打卡
  const [stop, setStop] = useState(false)
  const [stopId, setStopId] = useState('')

  // // 补打卡id
  // const [appealId, setAppealId] = useState('')
  // 补打卡id
  const [idea, setIdea] = useState('')

  function submit() {
    
    const stuInfo = {
      name: name,
      id: id,
      mobile: mobile,
      grade: grade,
      sex: sex,
      company: company,
      currentLocation: currentLocation,
      whetherInSchool: whetherInSchool,
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
    if(!reg.test(stuInfo.company) || reg1.test(stuInfo.company)){
      window.alert('学院应为汉字')
      return
    }
    // 简单的验证
    if(!((/\d{10}/.test(stuInfo.id) && stuInfo.id.length === 10) || 
         (/\d{12}/.test(stuInfo.id) && stuInfo.id.length === 12))){
      window.alert('学号应为10位或12位数字')
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
    
    axios({
      url: 'https://notzjw.top/autoAppeal/join',
      method: 'post',
      data: stuInfo,
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
      },
      reason => {
        window.alert(`加入失败, 原因: ${reason.message}`)
      }
    )

  }
  function modify() {
  
    const stuInfo = {
      name: name,
      id: id,
      mobile: mobile,
      grade: grade,
      sex: sex,
      company: company,
      currentLocation: currentLocation,
      whetherInSchool: whetherInSchool,
      emLinkPerson: emLinkPerson,
      emLinkMobile: emLinkMobile,
      auditName: auditName,
      auditId: '',
    }
    // 简单的验证
    if(!((/\d{10}/.test(stuInfo.id) && stuInfo.id.length === 10) || 
         (/\d{12}/.test(stuInfo.id) && stuInfo.id.length === 12))){
      window.alert('学号应为10位或12位数字')
      return
    }

    const reg = new RegExp("[\\u4E00-\\u9FFF]+")
    const reg1 = new RegExp("[a-zA-Z]+")
    let nomodify_message = ''
    let modify_message = '年级,性别,是否在校园内'
    if(!reg.test(stuInfo.name) || reg1.test(stuInfo.name)){
      nomodify_message += '姓名'
      stuInfo.name = ''
    }else{
      modify_message += '姓名,'
    }
    if(!reg.test(stuInfo.company) || reg1.test(stuInfo.company)){
      nomodify_message += '学院,'
      stuInfo.name = ''
    }else{
      modify_message += '学院,'
    }
    if(!reg.test(stuInfo.currentLocation) || reg1.test(stuInfo.currentLocation)){
      nomodify_message += '当前位置,'
      stuInfo.currentLocation = ''
    }else{
      modify_message += '当前位置,'
    }

    if(!/\d{11}/.test(stuInfo.mobile) || stuInfo.mobile.length !== 11){
      nomodify_message += '手机号,'
      stuInfo.mobile = ''
    }else{
      modify_message += '手机号,'
    }
    if(!reg.test(stuInfo.emLinkPerson) || reg1.test(stuInfo.emLinkPerson)){
      nomodify_message += '紧急联系人,'
      stuInfo.emLinkPerson = ''
    }else{
      modify_message += '紧急联系人,'
    }
    if(!/\d{11}/.test(stuInfo.emLinkMobile) || stuInfo.emLinkMobile.length !== 11){
      nomodify_message += '紧急联系人电话,'
      stuInfo.emLinkMobile = ''
    }else{
      modify_message += '紧急联系人电话,'
    }
    if(!reg.test(stuInfo.auditName) || reg1.test(stuInfo.auditName)){
      nomodify_message += '辅导员姓名,'
      stuInfo.auditName = ''
    }else{
      modify_message += '辅导员姓名,'
    }
    const message = '【本次修改】:\n' + modify_message + '\n\n【本次不修改】\n' + nomodify_message

    window.alert(message)
    axios({
      url: 'https://notzjw.top/autoAppeal/modify',
      method: 'post',
      data: stuInfo,
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
      },
      reason => {
        window.alert(`修改失败, 原因: ${reason.message}`)
      }
    )

  }
  function stopClock() {
    // 简单的验证
    if(!((/\d{10}/.test(stopId) && stopId.length === 10) || 
         (/\d{12}/.test(stopId) && stopId.length === 12))){
      window.alert('学号应为10位或12位数字')
      return
    }
    
    axios({
      url: 'https://notzjw.top/autoAppeal/stopClock',
      method: 'post',
      data: { id: stopId },
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
        
      },
      reason => {
        window.alert(`停止打卡失败, 原因: ${reason.message}`)
        
      }
    )
  }
  function search() {
    // 简单的验证
    if(!((/\d{10}/.test(stopId) && stopId.length === 10) || 
         (/\d{12}/.test(stopId) && stopId.length === 12))){
      window.alert('学号应为10位或12位数字')
      return
    }
    
    axios({
      url: 'https://notzjw.top/autoAppeal/search',
      method: 'post',
      data: { id: stopId },
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
        
      },
      reason => {
        window.alert(`查询信息失败, 原因: ${reason.message}`)
        
      }
    )
  }
  function sayToMe() {
    if(idea.length === 0){
      window.alert('不能为空')
      return
    }
    
    axios({
      url: 'https://notzjw.top/autoAppeal/saytome',
      method: 'post',
      data: { idea: idea },
      headers: { 'Content-Type': 'application/json' }
    }).then(
      resp => {
        window.alert(resp.data.message)
        setIdea('')
      },
      reason => {
        window.alert(`发生错误啦, 原因: ${reason.message}`)
      }
    )
  }

  // 自动获取当前位置
  if(currentLocation === ''){
    getCurrentPosition(setCurrentLocation)
  }
  
  return (
    <div className="App-container">
      <div className='whtie-block'></div>
      <h>私底下用用就好了🤫</h>
      <h>作者随时跑路🐸</h>
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

          <span className='field'>当前所在位置: </span>
          <input className='input' value={currentLocation} placeholder='xx省xx市xx区/县/市' type="text" onInput={(e) => setCurrentLocation(e.target.value)} />

          <span className='field'>今天是否在校园内: </span>
          <select className='input' defaultValue={'3'} onChange={(e) => setWhetherInSchool(e.target.value)} >
            <option value="1">今天在校园内</option>
            <option value="2">已离校，在杭州租房</option>
            <option value="3">已返乡</option>
          </select>

          <span className='field'>紧急联系人: </span>
          <input className='input' type="text" onInput={(e) => setEmLinkPerson(e.target.value)} />
          
          <span className='field'>紧急联系人电话: </span>
          <input className='input' type="tel" onInput={(e) => setEmLinkMobile(e.target.value)} />
          

          <span className='field'>辅导员: </span>
          <input className='input' type="text" onInput={(e) => setAuditName(e.target.value)} />
          

        </fieldset>
      </form>
      <div className='btn-group'>
        <button className='submit-btn btn' onClick={throttle(submit, 200)}>提交信息</button>
        <div className='modify-container'>
          <button className='modify-btn btn' onClick={throttle(modify, 200)}>修改信息</button>
          <span style={{'fontSize': 'x-small'}}>根据学号</span>
        </div>
      </div>

      {/* <div className='divid-line'></div> */}
      <div className='whtie-block'></div>

      <h className='title'>停止/启动自动打卡&emsp;||&emsp;查询信息</h>
      <fieldset  className='fieldset'>
        <span className='field'>学&emsp;号: </span>
        <input className='input' type="text" onInput={(e) => setStopId(e.target.value)}/>
      </fieldset>
      <div className='btn-group'>
        <button className='stop-btn btn' onClick={throttle(stopClock, 200)}>停止/启动</button>
        <button className='search-btn btn' onClick={throttle(search, 200)}>查询</button>
      </div>
      
      <div className='whtie-block'></div>

      <h className='title'>有什么想法大胆提出来吧！</h>
      <fieldset  className='fieldset'>
        <span className='field'>想&emsp;法: </span>
        <input className='input' value={idea} onInput={(e) => setIdea(e.target.value)}></input>
      </fieldset>
      <button className='say-btn btn' onClick={throttle(sayToMe, 200)}>提交</button>
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