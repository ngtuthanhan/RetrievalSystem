// @bekbrace
// FARMSTACK Tutorial - Sunday 13.06.2021
 
import React, { useState, useEffect} from 'react';
import VideoView from './components/VideoListView';
import axios from 'axios';

function App() {

  const [VideoList, setVideoList] = useState([{}])

  // Read all videos
  useEffect(() => {
    axios.get('http://localhost:8000/api/video',)
      .then(res => {
        setVideoList(res.data)
      })
  });
  return (
    <div><VideoView VideoList={VideoList} /></div>
  );
}

export default App;