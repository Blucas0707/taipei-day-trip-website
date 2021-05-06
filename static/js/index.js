/*
    MVC (Model-View-Controller)
    資料處理 - 畫面處理 - 控制流程
*/
//models
let models={
  data: null,
  nextPage:0,
  keyword:"",
  getkeywordsearch:function(){
    this.keyword = document.querySelector("#keyword").value;
    let url = "/api/attractions" + "?page=" + this.nextPage + "&keyword=" + this.keyword;
    return fetch(url).then((response) => {
      return response.json();
    }).then((result) => {
      this.data = result;
      console.log(this.data);
    });
  },
  getProductData:function(){
    let url = "/api/attractions" + "?page=" + this.nextPage + "&keyword=" + this.keyword;
    return fetch(url).then((response) => {
      return response.json();
    }).then((result) => {
      this.data = result;
      console.log(this.data);
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
    //login/register or cancel login
    controller.login();
    controller.cancelLogin();

  }

};
//controllers
let controller={
  cancelLogin:function(){
    let cancelLoginbtn = document.querySelector(".login-cancel");
    cancelLoginbtn.addEventListener("click",views.cancelLogin);
  },
  login:function(){
    let login = document.querySelector(".nav-login");
    login.addEventListener("click",views.showLogin);
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
    models.getProductData().then(()=>{
      views.renderData();
    });
  }
};

controller.init();
