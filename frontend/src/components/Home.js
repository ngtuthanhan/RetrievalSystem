import React, {useState} from 'react';
import VideoView from './VideoListView';
import axios from 'axios';


function Home() {

  const [VideoList, setVideoList] = useState([{}])

  const [formData, setFormData] = useState({
    Vietnamese: '',
    English: '',
  });

  const handleInputChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(formData)
    axios
      .post('http://localhost:8000/api/video/', formData)
      .then((res) => {   
          setVideoList(res.data)
      })
      .catch((error) => {
        // Handle errors
        console.error(error);
      });
  };
  
  return (
    

    <div class="d-md-flex align-items-stretch">
      <nav id="sidebar">
        <form onSubmit={handleSubmit}
          class="subscribe-form p-4">
          <div class="form-group d-flex" data-validate="Text description is
            required">
            <textarea class="icon form-control" name="Vietnamese"
              placeholder="Vietnamese desciption" value={formData.Vietnamese}
              onChange={handleInputChange}></textarea>
            <span class="icon-paper-plane"></span>
          </div>
          <div class="form-group d-flex" data-validate="Text description is
            required">
            <textarea class="icon form-control" name="English"
              placeholder="English desciption" value={formData.English}
              onChange={handleInputChange}></textarea>
            <span class="icon-paper-plane"></span>
          </div>
 
          <div class="container-contact1-form-btn">
            <button class="contact1-form-btn">
              <span>
                Search
              </span>
            </button>
          </div>
        </form>
        <div class="border-top p"></div>
        <p id="result" class="passage"></p>
      </nav>
    <div id="content" class="content-custom"><VideoView VideoList={VideoList} /> </div>
  </div>
      
  );
}

export default Home;