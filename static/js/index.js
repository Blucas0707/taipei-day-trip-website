/*
    MVC (Model-View-Controller)
    資料處理 - 畫面處理 - 控制流程
*/
//models
let models={
  data: null,
  nextPage:0,
  keyword:"",
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
  getkeywordsearch:function(){
    this.keyword = document.querySelector("#keyword").value;
    let url = "/api/attractions" + "?page=" + this.nextPage + "&keyword=" + this.keyword;
    return fetch(url).then((response) => {
      return response.json();
    }).then((result) => {
      this.data = result;
      // console.log(this.data);
    });
  },
  getProductData:function(){
    let url = "/api/attractions" + "?page=" + this.nextPage + "&keyword=" + this.keyword;
    return fetch(url).then((response) => {
      return response.json();
    }).then((result) => {
      this.data = result;
      // console.log(this.data);
    });
  }
};
//views
let views={
  clear:function(){
    let img = document.querySelector(".image-gallery");
    while (img.firstChild) {
      img.removeChild(img.firstChild);
    }
    models.nextPage = 0;
  },
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
    let navLogout = document.querySelector(".nav-logout");
    if(models.loginData != null){ //get session success
      navLogin.style.display = "none";
      navLogout.style.display = "block";
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
  },
  cancelLogin:function(){
    let hideall = document.querySelector(".hideall");
    hideall.style.display="none"; //隱藏hide
    let loginBox = document.querySelector(".login-box");
    loginBox.style.display="none"; //隱loginBox
    let registerBox = document.querySelector(".register-box");
    registerBox.style.display="none";  //隱藏register box
  },
  scrolldown:function(){
    let need_scrolldown = true;
    //count scroll down ration > 90% load more next_page
    var scrollTop = window.pageYOffset;
    var bodyHeight = document.querySelector(".body").getBoundingClientRect().height;
    var windowHeight = window.screen.height;
    var totalScroll = scrollTop + windowHeight;
    //judge load completed
    if(totalScroll > bodyHeight * 0.95 && models.nextPage!=null && need_scrolldown){
      need_scrolldown = false;
      models.getProductData().then(views.renderData);
      need_scrolldown = true;
    }
  },
  renderData:function(){
    let id, name, mrt, category, image,nextPage, dataLength;
    models.nextPage = models.data.nextPage;
    //no data
    if(models.nextPage!=null){
      dataLength = models.data.data.length;
      for(let index = 0;index<dataLength;index++){
        id = models.data.data[index].id;
        name = models.data.data[index].name;
        mrt = models.data.data[index].mrt;
        category = models.data.data[index].category;
        image = models.data.data[index].images[0];

        // create new div under img-gallery
        div = document.createElement('div');
        div.className = 'img';
        div.id = 'view';
        div.id = id;
        div_img_gallery = document.querySelector('#img-gallery-contain');
        div_img_gallery.appendChild(div);

        // create new img under new div
        img = document.createElement('img');
        img.src = image;
        div.appendChild(img);

        // create new div block
        div_block = document.createElement('div');
        div_block.className = "image-block";
        div.appendChild(div_block);

        // create new name-div under new div
        div_name = document.createElement('div');
        div_name.className = "image-name";
        div_block.appendChild(div_name);
        content = document.createTextNode(name);
        div_name.appendChild(content);

        // create new div description under new div
        div_description = document.createElement('div');
        div_description.className = "image-description";
        div_block.appendChild(div_description);

        // create new span mrt under new div
        span_mrt = document.createElement('span');
        span_mrt.className = "image-mrt";
        div_description.appendChild(span_mrt);
        content = document.createTextNode(mrt);
        span_mrt.appendChild(content);

        // create new span category under new div
        span_category = document.createElement('span');
        span_category.className = "image-category";
        div_description.appendChild(span_category);
        content = document.createTextNode(category);
        span_category.appendChild(content);
      }
    }
    else if(models.nextPage==null && document.querySelector(".img") == null){
      div = document.createElement('div');
      div.className = 'nodata';
      body = document.querySelector('#img-gallery-contain');
      body.appendChild(div);
      document.querySelector(".nodata").innerHTML = "此次搜尋，沒有結果";
    }

    //scroll down
    window.addEventListener("scroll", this.scrolldown);

    // get keywordSearch
    let btn_keyword = document.querySelector(".keyin_Keyword");
    btn_keyword.addEventListener("click",controller.keywordSearch);
    //click img
    controller.imgClick();
    //login/register or cancel
    controller.loginRegister();
    controller.cancelLoginRegister();
    // check login & logout
    controller.userRegister(); // user register btn
    controller.userLogin(); // user login btn
    controller.checkLogout();

  }

};
//controllers
let controller={
  checkLogout:function(){
    let logout = document.querySelector(".nav-logout");
    logout.addEventListener("click",()=>{
      models.checkUserLogout().then(()=>{
        views.renderLogout();
      });
    });
  },
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
  imgClick:function(){
    let imgs = document.querySelectorAll("div.img");
    for(let i = 0;i<imgs.length;i++){
      let url = "/attraction/" + imgs[i].id;
      imgs[i].addEventListener("click", function(e){
        window.location.replace(url);
      });
    }
  },
  keywordSearch:function(){
    //clear
    views.clear();
    models.getkeywordsearch().then(()=>{
      views.renderData();
    });
  },
  init:function(){
    this.checkLogin();//check login session
    models.getProductData().then(()=>{ //get product pic
      views.renderData();
    });
  }
};

controller.init();
