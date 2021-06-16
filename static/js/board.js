/*
    MVC (Model-View-Controller)
    資料處理 - 畫面處理 - 控制流程
  */

function filename_now(){
  let time = new Date();
  let year = time.getFullYear();
  let month = time.getMonth()+1;
  let date = time.getDate();
  let hour = time.getHours();
  let min = time.getMinutes();
  let sec = time.getSeconds();
  let minsec = time.getMilliseconds();
  let filename = year+"-"+month+"-"+date+"-"+hour+"-"+min+"-"+sec+"-"+minsec;
  return filename;
};

//models
let model ={
  ContentData:null,
  updateData:null,
  uploadData:function(text, img){
    let filename = filename_now()+"."+img.type.substr(6,);;
    // console.log(text,img,filename);
    let form = new FormData();
    form.append("comment",text);
    form.append("img",img, filename);
    // console.log(form);
    fetch("/api/board",{
      method:"POST",
      body:form,
    }).then((response)=>{
      return response.json();
    }).then((result)=>{
      model.updateData = result;
      // console.log(result);
      view.renderUpload();
    })
  },
  getAllDate:function(resolve){
    fetch("/api/board",{
      method:"GET",
    }).then((response)=>{
      return response.json();
    }).then((result)=>{
      model.ContentData = result;
      // console.log(model.ContentData);
      resolve(true);
    })
  },
};
//view
let view = {
  renderData:function(){
    let p = new Promise(model.getAllDate);
    p.then(()=>{
      // console.log("get data ok");
      let content_div = document.querySelector(".content-display");
      for(let i=0;i< model.ContentData.total; i++){
        let record_box = document.createElement("div");
        record_box.className = "record_box";
        let text_div = document.createElement("div");
        text_div.className = "content-text";
        text_div.innerHTML = model.ContentData.content[i].text;
        record_box.appendChild(text_div);

        let img_div = document.createElement("img");
        img_div.className = "content-img";
        img_div.src = model.ContentData.content[i].img_link;
        record_box.appendChild(img_div);

        // add record box to Content
        content_div.append(record_box);
        // console.log(i,model.ContentData.content[i].text,model.ContentData.content[i].img_link);

      };
    });
  },
  renderUpload:function(){
    // console.log("get data ok");

    //loading img
    document.querySelector(".loading").style.display = "none";

    let content_div = document.querySelector(".content-display");
    //record box for text & img
    let record_box = document.createElement("div");
    record_box.className = "record_box";

    //text div
    let text_div = document.createElement("div");
    text_div.className = "content-text";
    text_div.innerHTML = model.updateData.comment;
    record_box.appendChild(text_div);
    //img div
    let img_div = document.createElement("img");
    img_div.className = "content-img";
    img_div.src = model.updateData.img_link;
    record_box.appendChild(img_div);

    // add record box to Content as first child
    content_div.prepend(record_box);
    // console.log(i,model.updateData.content[0].text,model.initData.content[i].img_link);
  },
};
//controller
let controller ={
  inputText:null,
  inputImage:null,
  upload:function(resolve){
    let submitBtn = document.querySelector(".submit");
    submitBtn.addEventListener("click",()=>{
      let text = document.querySelector("#text-input").value;
      let img = document.querySelector("#image-input");

      if(text == "" || img.value == ""){
        document.querySelector(".error").style.display = "flex";
      }
      else{
        //loading img
        document.querySelector(".loading").style.display = "flex";
        //error
        document.querySelector(".error").style.display = "none";

        model.uploadData(text,img.files[0]);
        //clear
        document.querySelector("#text-input").value = "";
        document.querySelector("#image-input").value = "";
      }
    });
  },
  init:function(){
    view.renderData();
    controller.upload();
  }
};



controller.init();
// controller.upload();
