export default function VideoView(props) {
    const VideoList = props.VideoList
    console.log(VideoList[0])
    if (VideoList[0] === {}){
        return (<div> </div>)
    }
    return (
        <div id="content" class="content-custom">
        <div class="wrapper">
            {VideoList.map(video =>  
            <div class="">
            <input type="checkbox" id={"myCheckbox_"+video.keyframe}
                video={video.video} frame={video.frame_id}/>
            <label for={"myCheckbox_"+video.keyframe} class="label-checkbox">
                <img src={"http://localhost:8000/data/keyframe/"+video.keyframe}
                alt={video.keyframe}/>
                <div class="bottom-left">{video.video}</div>
                <div class="bottom-right">{video.frame_id}</div>
                <div class="top-right">
                <a class="detail-form-btn" href={"/knn/"+video.keyframe}>
                    <span>
                    KNN
                    </span>
                </a>
                </div>

                <div class="top-left">
                <a class="detail-form-btn" href={"/detail/"+video.keyframe}>
                    <span>
                    Detail
                    </span>
                </a>
                </div>
                </label>
            </div>
            )}
        </div>
        </div>
        
    )
    
}