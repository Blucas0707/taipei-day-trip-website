/*
    MVC (Model-View-Controller)
    資料處理 - 畫面處理 - 控制流程
  */
//models
let models = {
  data: null,
  loginData:null,
  logoutData:null,
  regsiterData:null,
  checkUserLogout:function(){
    return fetch("/api/user",{
      method:"DELETE"
    }).then((response)=>{
      return response.json();
    }).then((result)=>{
      this.logoutData = result;
      this.loginData = null;
      // console.log(this.loginData);
    })
  },
  checkUserLogin:function(){
    return fetch("/api/user",{
      method:"GET"
    }).then((response)=>{
      return response.json();
    }).then((result)=>{
      this.loginData = result;
      this.logoutData = null;
      // console.log(this.loginData);
    });
  },
  validateRegister:function(){
    let formElement = document.querySelector("#register-form");
    let name = formElement.name.value;
    let email = formElement.email.value;
    let password = formElement.password.value;
    // regular rules
    var emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
    let emailCheck = true;
    let nameCheck = true;
    let passwordCheck = true;
    emailCheck = email.search(emailRule) == 0; //check email format
    nameCheck = name.length >= 4; //check name length >= 4
    passwordCheck = password.length >= 6; //check password >= 6
    // console.log(emailCheck,nameCheck,passwordCheck);
    this.regsiterData = {
      "name":nameCheck,
      "email":emailCheck,
      "password":passwordCheck
    };

    return nameCheck&&emailCheck&&passwordCheck;

  },
  getuserRegister:function(){
    let formElement = document.querySelector("#register-form");
    let name = formElement.name.value;
    let email = formElement.email.value;
    let password = formElement.password.value;
    let data = {
        "name":name,
        "email":email,
        "password":password
      };
    return fetch("/api/user",{
      method:"POST",
      headers: {"Content-type":"application/json;"},
      body: JSON.stringify(data)
    }).then((response)=>{
      return response.json();
    }).then((result)=>{
      this.regsiterData = result;
    });

  },
  validateLogin:function(){
    let email = document.querySelector(".login-email").value;
    let password = document.querySelector(".login-password").value;
    // regular rules
    // var emailRule = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
    let emailCheck = true;
    let passwordCheck = true;
    emailCheck = email.length > 0; //check email format
    passwordCheck = password.length > 0; //check password >= 0
    // console.log(emailCheck,passwordCheck);
    this.loginData = {
      "email":emailCheck,
      "password":passwordCheck
    };

    return emailCheck&&passwordCheck;

  },
  getuserLogin:function(){
    // let formElement = document.querySelector("#login-form");
    // let email = formElement.email.value;
    // let password = formElement.password.value;
    let email = document.querySelector(".login-email").value;
    let password = document.querySelector(".login-password").value;
    let data = {
      "email":email,
      "password":password
    };
    // console.log(email,password);
    return fetch("/api/user",{
      method:'PATCH',
      headers: {"Content-type":"application/json;"},
      body: JSON.stringify(data),
    }).then((response)=>{
      // console.log(response.json());
      return response.json();
    }).then((result)=>{

      this.loginData = result;
      // console.log(result);
    });
  },
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
  renderLogout:function(){
    let navLogin = document.querySelector(".nav-login");
    let navLogout = document.querySelector(".nav-logout");
    if(models.logoutData != null){ //get session success
      navLogin.style.display = "block";
      navLogout.style.display = "none";
    }
  },
  renderLogin:function(){
    let navLogin = document.querySelector(".nav-login");
    // let navLogout = document.querySelector(".nav-logout");
    if(models.loginData != null){ //get session success
      // navLogin.style.display = "none";
      // navLogout.style.display = "block";
      navLogin.innerHTML = "登出系統";
    }else{
      navLogin.innerHTML = "註冊/登入";
    }
  },
  renderLoginValidation:function(){
    let loginstatus = document.querySelector(".login-status");
    loginstatus.style.display = "block";
    if(models.loginData.name == false || models.loginData.password == false){
      loginstatus.innerHTML = "帳號或密碼不得為空";
    }
  },
  LoginStatus:function(){
    let loginstatus = document.querySelector(".login-status");
    loginstatus.style.display = "block";
    if(models.loginData != null){
      if(models.loginData.error == true ){
        loginstatus.innerHTML = "登入失敗，帳號或密碼錯誤";
      }
      else{
        loginstatus.innerHTML = "登入成功";
        window.location.reload(); // reload
      }
    }
  },
  renderRegisterValidation:function(){
    let registerstatus = document.querySelector(".register-status");
    registerstatus.style.display = "block";
    if(models.regsiterData.name == false){
      registerstatus.innerHTML = "姓名長度必須大於4";
    }
    else if (models.regsiterData.email == false) {
      registerstatus.innerHTML = "電子信箱格式有誤";
    }
    else if (models.regsiterData.password == false) {
      registerstatus.innerHTML = "密碼長度亦須大於6";
    }
  },
  RegisterStatus:function(){
    let registerstatus = document.querySelector(".register-status");
    registerstatus.style.display = "block";
    if(models.regsiterData.error == true){
      registerstatus.innerHTML = "註冊失敗，電子信箱已被註冊";
    }
    else{
      if(models.regsiterData.ok == true){
        registerstatus.innerHTML = "註冊成功，請重新登入";
      }
      else{
        if(models.regsiterData.name == false){
          registerstatus.innerHTML = "姓名必須大於4個字元";
        }else if (models.regsiterData.email == false) {
          registerstatus.innerHTML = "電子郵件格式錯誤";
        }else if (models.regsiterData.password == false) {
          registerstatus.innerHTML = "密碼必須大於6個字元";
        }
      }
    }
  },
  showRegister:function(){
    let loginBox = document.querySelector(".login-box");
    loginBox.style.display = "none"; //隱藏loginBox
    let registerBox = document.querySelector(".register-box");
    registerBox.style.display = "block"; //show registerBox

    let registerStatus = document.querySelector(".register-status"); //clear login/register status
    let loginStatus = document.querySelector(".login-status");
    registerStatus.style.display = "none";
    loginStatus.style.display = "none";
  },
  showLogin:function(){
    let login = document.querySelector(".nav-login");
    if(login.innerHTML == "註冊/登入"){
      let hideall = document.querySelector(".hideall");
      hideall.style.display="block";  //顯示隱藏層
      hideall.style.height=document.body.clientHeight+"px";  //設定隱藏層的高度為當前頁面高度   px是字尾

      let loginBox = document.querySelector(".login-box");
      loginBox.style.display = "block"; //顯示彈出層
      let registerBox = document.querySelector(".register-box");
      registerBox.style.display = "none"; //隱藏 registerBox

      let registerStatus = document.querySelector(".register-status"); //clear login/register status
      let loginStatus = document.querySelector(".login-status");
      registerStatus.style.display = "none";
      loginStatus.style.display = "none";
    }else{
      login.style.display = "block";
      login.innerHTML = "註冊/登入";
      models.checkUserLogout(); //logout & delete session
    }

  },
  cancelLogin:function(){
    let hideall = document.querySelector(".hideall");
    hideall.style.display="none"; //隱藏hide
    let loginBox = document.querySelector(".login-box");
    loginBox.style.display="none"; //隱loginBox
    let registerBox = document.querySelector(".register-box");
    registerBox.style.display="none";  //隱藏register box
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
  },

};
//controller
let controller = {
  checkLogin:function(){
    models.checkUserLogin().then(()=>{
      views.renderLogin();
    });
  },
  userRegister:function(){
    let register = document.querySelector(".register-btn");
    register.addEventListener("click",()=>{
      let validation = models.validateRegister(); //驗證註冊資料
      // console.log(validation);
      if(validation){
        models.getuserRegister().then(()=>{
          views.RegisterStatus();
        });
      }else{
        views.renderRegisterValidation();
      }
    });
  },
  userLogin:function(){
    let login = document.querySelector(".login-btn");
    login.addEventListener("click",()=>{
      let validation = models.validateLogin(); //驗證登入資料
      // console.log(validation);
      if(validation){
        models.getuserLogin().then(()=>{
          views.LoginStatus();
        });
      }else{
        views.renderLoginValidation();
      }
    });
  },
  cancelLoginRegister:function(){
    let cancelLoginbtn = document.querySelector(".login-cancel");
    let cancelRegisterbtn = document.querySelector(".register-cancel");
    cancelLoginbtn.addEventListener("click",views.cancelLogin);
    cancelRegisterbtn.addEventListener("click",views.cancelLogin);
  },
  loginRegister:function(){

    let loginBox = document.querySelector(".nav-login"); //index to loginBox
    loginBox.addEventListener("click",views.showLogin);

    let register = document.querySelector(".login-register"); //loginBox to RegisterBox
    register.addEventListener("click",views.showRegister);

    let loginbtn =  document.querySelector(".login-btn"); //login btn
    loginbtn.addEventListener("click",this.userLogin);

    let backtologin = document.querySelector(".register-login"); // registerBox to loginBox
    backtologin.addEventListener("click",views.showLogin);
  },
  // Choose package data
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
  init:function(){
    this.checkLogin();//check login session
    models.getData().then(()=>{ //get product pic
      views.renderData();
    });
  }
}

controller.init();
//login/register or cancel
controller.loginRegister();
controller.cancelLoginRegister();
// check login & logout
controller.userRegister(); // user register btn
controller.userLogin(); // user login btn
// controller.checkLogout();
