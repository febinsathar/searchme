import React, { Component } from 'react';
import './App.css';
import 'spectre.css'
import { connect } from 'react-redux'
import SpectreAutocomplete from './component/spectreAutocomplete'

const commonStyles = {
  textAlign: "center"
};
class App extends Component {
  constructor() {
    super();
    this.state = {
      loaderWidth:20,
      searching:false
    };
  }
  timer() {
    this.setState({
      loaderWidth: this.state.loaderWidth +10
    })
  }
  componentDidMount() {
    // this.intervalId = setInterval(this.timer.bind(this), 100);
    // this.setState({intervalId: this.intervalId});

  }
  componentWillUnmount(){
    // clearInterval(this.intervalId);
  }
  render() {
    return (
      <div>
      {/* <div className="bar bar-sm">
      <div className="bar-item" role="progressbar" style={{width:this.state.loaderWidth}} aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
    </div> */}
    
    {/* {this.props.searching? <div className="loading loading-lg"></div>:null } */}
      <div style={{margin: "50px auto",maxWidth: 800,marginTop:100}}>


      <h1 style={commonStyles}>Word Autocomplete</h1>
      <br />
      <div
        className="form-autocomplete"
        style={{ margin: "auto", maxWidth: 600 }}
      >
        <SpectreAutocomplete />
      </div>
      <br />
    </div>
    </div>
    );
  }
}


function mapStateToProps(state) {
  const { searching } = state.searchReducer
  return {
    searching
  }
}
export default connect(mapStateToProps,null)(App)