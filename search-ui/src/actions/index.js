// index.js

import { SEARCHING,SEARCH_SUCESS,SEARCH_FAIL } from './types';
import axios from 'axios';

const apiUrl = '/search?word=';


export const onSearchSucess = (resp) => {
  return {
    type: SEARCH_SUCESS,
    payload:resp,
    receivedAt: Date.now()
  }
};

export const searching = (status) => {
    return {
      type: SEARCHING,
      searching:status,
      receivedAt: Date.now()
        
    }
  };
  

export const onSearchFail = (error) => {
    return {
      type: SEARCH_FAIL,
      error,
      receivedAt: Date.now()
    }
  };

export const searchMe = (searchTerm,pageStart,pageEnd) => {
  return (dispatch) => {
    if(!searchTerm || searchTerm.length===0 || searchTerm===""){
        dispatch(onSearchSucess({"result":[],"total":0,"time":"0s"}))
    }else{
        dispatch(searching({searching:true}));
        return axios.get(`${apiUrl}${searchTerm}&page_start=${pageStart}&page_end=${pageEnd}`)
          .then(response => {
            dispatch(searching({searching:false}));
            dispatch(onSearchSucess(response.data))
          })
          .catch(error => {
            dispatch(searching({searching:false}));
            dispatch(onSearchFail(error));
            throw(error);
          });

    }

  };
};