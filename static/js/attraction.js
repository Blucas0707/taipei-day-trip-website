/*
    MVC (Model-View-Controller)
    資料處理 - 畫面處理 - 控制流程
  */
//models
let models = {
  data: null,
  getData: function() {
    let url = "/api/" + location.pathname;
    return fetch(url).then((response) => {
      return response.json();
    }).then((result) => {
      this.data = result.data;
      // console.log(this.data);
    });
  }
};
//views
let views = {
  images:null,
  imageIndex:0,
  showLogin:function(){
    let hideall = document.querySelector(".hideall");
    hideall.style.display="block";  //顯示隱藏層
    hideall.style.height=document.body.clientHeight+"px";  //設定隱藏層的高度為當前頁面高度   px是字尾
    let loginBox = document.querySelector(".login-box");
    loginBox.style.display = "block"; //顯示彈出層
  },
  cancelLogin:function(){
    let hideall = document.querySelector(".hideall");
    hideall.style.display="none";
    let loginBox = document.querySelector(".login-box");
    loginBox.style.display="none";
  },
  renderImageorder:function(){
    //remove all child first
    div = document.querySelector(".img-order");
    while (div.firstChild) {
      div.removeChild(div.firstChild);
    }
    //add new child for img order dot
    for(let order = 0 ; order < this.images.length; order++){
      const li = document.createElement("li");
      if(order == this.imageIndex){
        li.className = "img-order-pick";
      }
      else{
        li.className = "img-order-list";
      }
      div.appendChild(li);
    };
  },
  renderData: function() {
    let name, mrt, category, description, address, transport, images, div;
    name = models.data.name;
    mrt = models.data.mrt;
    category = models.data.category;
    description = models.data.description;
    address = models.data.address;
    transport = models.data.transport;
    this.images = models.data.images;
    // location
    div = document.querySelector(".name");
    div.textContent = name;
    // category + mrt
    div = document.querySelector(".location");
    div.textContent = category + " at " + mrt;
    //content (description)
    div = document.querySelector(".content");
    div.textContent = description;
    //address-content
    div = document.querySelector(".address-content");
    div.textContent = address;
    //traffic-content
    div = document.querySelector(".traffic-content");
    div.textContent = transport;
    //images
    div = document.querySelector(".img");
    const img = document.createElement("img");
    img.className = "img-pic";
    img.src = this.images[this.imageIndex];
    div.appendChild(img);
    //show img order dot
    this.renderImageorder();

    // choose package;
    controller.choosePackage();
    controller.clickImage();

    //login/register or cancel login
    controller.login();
    controller.cancelLogin();
  },

};
//controller
let controller = {
  cancelLogin:function(){
    let cancelLoginbtn = document.querySelector(".login-cancel");
    cancelLoginbtn.addEventListener("click",views.cancelLogin);
  },
  login:function(){
    let login = document.querySelector(".nav-login");
    login.addEventListener("click",views.showLogin);
  },
  choosePackage:function(){
    const timeUp = document.querySelector("#timeUp");
    const timeDown = document.querySelector("#timeDown");
    const totalFee = document.querySelector(".total-fee");
    timeUp.addEventListener("click",()=>{
      totalFee.innerHTML = "新台幣 2000元";
    });
    timeDown.addEventListener("click",()=>{
      totalFee.innerHTML = "新台幣 2500元";
    });
  },
  clickImage:function(){
    const imgLeft = document.querySelector(".img-left");
    const imgRight = document.querySelector(".img-right");
    const img = document.querySelector(".img-pic");
    //click left
    imgLeft.addEventListener("click",()=>{
      views.imageIndex -= 1;
      if(views.imageIndex < 0 ){
        views.imageIndex = views.images.length-1;
      }
      views.renderImageorder();
      img.src = views.images[views.imageIndex];
    });
    //click right
    imgRight.addEventListener("click",()=>{
      views.imageIndex += 1;
      if(views.imageIndex > views.images.length-1 ){
        views.imageIndex = 0;
      }
      views.renderImageorder();
      img.src = views.images[views.imageIndex];
    });

  },
  init: function() {
    models.getData().then(()=>{
      views.renderData();
    });
  }
}
controller.init();
