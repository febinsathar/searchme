// postReducer.js

import { SEARCHING,SEARCH_SUCESS,SEARCH_FAIL  } from '../actions/types';

const intialState={
  availableWords:[],
  searching:false,
  totalRecords:0,
  time:"0s",
  pageStart:0,
  pageEnd:0,
  pageSize:25,
  page:-1

}

 const searchReducer =(state=intialState, action)=> {
  switch (action.type) {
    case SEARCHING:
      return {...state, searching:true,error:false,pageStart:0,pageEnd:0,totalRecords:0};
    case SEARCH_SUCESS:
      return {...state, availableWords:action.payload['result'],
      searching:false,error:false,totalRecords:action.payload['totalRecords'],
      time:action.payload['time'],pageStart:action.payload['pageStart'],pageEnd:action.payload['pageEnd']}
    case SEARCH_FAIL:
      return {...state,availableWords:[],searching:false,error:true,pageStart:0,pageEnd:0,totalRecords:0}
    default:
      return state;
  }
}
export default searchReducer;