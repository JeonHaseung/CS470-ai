import React, { Component } from 'react';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    this.textareaPlaceHolder = 'Please enter your text';
    this.text1 = '';
    this.text2 = '';
  }

  getTitle = () => {
    return (
      <div className='title'>
        <div className='title-yellow'>{'H'}</div>
        <div className='title-white'>{'ot  '}</div>
        <div className='title-yellow'>{'I'}</div>
        <div className='title-white'>{'ssue'}</div>
      </div>
    )
  };

  submitTexts = () => {
    const body = { 'text1': this.text1, 'text2': this.text2 };

    const text1Box = document.getElementById('text1');
    const text2Box = document.getElementById('text2');
    text1Box.style.border = '15px solid transparent';
    text2Box.style.border = '15px solid transparent';

    // fetch('http://143.248.135.38:8000/inference', {
    // fetch('http://172.30.1.7:8000/inference', {
    fetch('http://localhost:8000/inference', {
      method: 'post',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    })
      .then(response => response.json())
      .then(data => {
        console.log(data, data.result === "1");
        if (data.result === "0") {
          text1Box.style.border = '15px solid red';
        }
        else {
          text2Box.style.border = '15px solid red';
        }

        // setTimeout(() => {
        //   window.confirm('Is it same with your opinion?\n(Yes->ok / No->cancel)');
        //   alert('Thank you for participating')
        // }, 500);
      });
  };

  enterText = (event, type) => {
    const text = event.target.value || '';

    if (type === 1) {
      this.text1 = text;
    }
    else {
      this.text2 = text;
    }
  };

  render() {
    return (
      <div className='container'>
        { this.getTitle() }

        <div className='textarea-box'>
          <textarea
            id='text1'
            rows='8'
            placeholder={this.textareaPlaceHolder}
            maxLength='140'
            onChange={(e) => this.enterText(e, 1)}
          />

          <textarea
            id='text2'
            rows='8'
            placeholder={this.textareaPlaceHolder}
            maxLength='140'
            onChange={(e) => this.enterText(e, 2)}
          />
        </div>

        <div
          className='submit-button'
          onClick={() => this.submitTexts()}
        >
          {'Submit!!'}
        </div>
      </div>
    )
  }
}

export default App;
