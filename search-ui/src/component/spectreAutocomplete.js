
import { render } from "react-dom";
import React, { Component } from "react";
import Downshift from "downshift";
import debounce from 'lodash/debounce';
import { connect } from 'react-redux'
import {searchMe} from '../actions/'


class SpectreAutocomplete extends Component {
  constructor() {
    super();
    this.state = {
      searchString:"",
      page:-1,
      pageStart:0,
      pageEnd:0,
    };
  }


  componentDidMount() {
    this.calculateNextPage(0)
  }
  clearInputValue=()=> {
    this.downshift.clearSelection();
  }
  clickChange=(item, clearSelection) =>{
    clearSelection()
  }

  setSearchTerm = debounce(searchTerm => {
    this.props.searchMe(searchTerm,0,25)
}, 500)
  
  keyboardChange(searchTerm) {
    this.setState({searchString: searchTerm})
      this.setSearchTerm(searchTerm)  
  }
  calculateNextPage = (action)=> {

    let prevPageStart= this.props.pageStart
    let prevPageEnd= this.props.pageEnd
    let pageSize= this.props.pageSize
    let totalRecord=this.props.totalRecords
    let pageStart=0
    let pageEnd=0

    if(action==1 ){
      pageStart=prevPageStart+pageSize
      pageEnd=pageStart+pageSize
      if(pageEnd>totalRecord){
        totalRecord=totalRecord
        pageStart=Math.floor(totalRecord/pageSize)*pageSize
      }
    }else if(action==-1){
      pageStart=prevPageStart-pageSize
      pageEnd=prevPageStart
      if(pageStart<0){
        pageStart=0
        pageEnd=pageSize
      }
    }
    if((prevPageStart!==pageStart) &(prevPageEnd!==pageEnd)){

        if(pageEnd>pageStart){
          console.log("calmee",pageStart,pageEnd)
          this.props.searchMe(this.state.searchString,pageStart,pageEnd)
        }

    }    

   }
    

  render() {

    let availableWords=this.props.availableWords
    let total = this.props.totalRecords
    let time = this.props.time
    let itemlength=availableWords.length||0
    return (
      <div>
      <p>
        <span> Showing  {this.props.pageStart} - {this.props.pageEnd} / {total} results ({time}) </span>
        <button 
          className="btn btn-action s-circle"
          onClick={() => this.calculateNextPage(-1)}>
          <i className="icon icon-arrow-left"></i></button>
        <span> &nbsp; &nbsp;</span>
        <button 
          className="btn btn-action s-circle"
          onClick={() => this.calculateNextPage(1)}>
          <i className="icon icon-arrow-right"></i></button>
      </p>
      <Downshift
       isOpen={itemlength>0} 
        onChange={word => ()=>{}}
      >
        {({
          clearSelection,
          getDownshiftStateAndHelpers,
          getInputProps,
          getItemProps,
          setInputProps,
          isOpen,
          inputValue,
          selectedItem,
          highlightedIndex
        }) => (
          <div className="form-autocomplete-input form-input">
            <input
              className="form-input"
              value={this.state.searchString} 
              onChange={e => {this.keyboardChange(e.target.value)}}
              type="text"
              placeholder="Search your word..."
            />
            {(isOpen && (
              <div className="menu">
                {(() => {
                  return [...this.props.availableWords, "No matches!"]
                    .map((item, index, arr) => (
                      <SpectreItem
                        {...getItemProps({ item, index })}
                        key={index}
                        isActive={highlightedIndex === index}
                        onClick={() => this.clickChange(item, clearSelection)}
                      >
                        {item}
                      </SpectreItem>
                    ));
                })()}
              </div>
            )) ||
              (!isOpen && <div />)}
          </div>
        )}
      </Downshift>
      </div>
    );
  }
}

const SpectreItem = ({ children, value, index, isActive, onClick }) => (
  <div
    className="menu-item"
    style={isActive ? { backgroundColor: "#eee" } : {}}
    onClick={onClick}
  >
    <a href="#!">
      <div className="tile tile-centered">
      <div className="tile-content">
    <div className="tile-title">{children.word}</div>
    <small className="tile-subtitle text-gray">{children.freq}</small>
  </div>
 
      </div>
    </a>
  </div>
);

const mapDispatchToProps = dispatch => ({
  searchMe: (searchTerm,pageStart,pageEnd) => dispatch(searchMe(searchTerm,pageStart,pageEnd))
})


function mapStateToProps(state) {
  const { availableWords, searching,totalRecords,time,pageStart,pageEnd,pageSize,page } = state.searchReducer
  return {
    availableWords,
    searching,
    totalRecords,
    time,
    page,
    pageStart,
    pageEnd,
    pageSize
  }
}
export default connect(mapStateToProps,mapDispatchToProps)(SpectreAutocomplete)