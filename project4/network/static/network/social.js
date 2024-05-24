
document.addEventListener("DOMContentLoaded",() =>{
   try{
      commentDiv = document.getElementById("comments")
      postID = commentDiv.getAttribute("data-post-id")
      loadComments(postID)
   } catch {
    console.log({Error: "Not Available in DOM"})
   }
})




const heartColor = (element) => {
  const id = element.id
 
  const heart = document.getElementById(`${id}`);
  postID = id.replace("heart","");
  console.log(postID)
 
  if(heart.getAttribute("fill") === "gray") {
    heart.setAttribute("fill","red");
    postLikes(postID,true)
    addLikes(`${postID}LIKE`,true)
  } else {
    
    postLikes(postID,false)
    addLikes(`${postID}LIKE`,false)
    heart.setAttribute("fill","gray")
    
  }
}
const handleSubmit = (event,post=null) => {
  event.preventDefault();
  id = event.target.id.replace("form","")
  content = document.getElementById(`${id}comment`).value;
  fetch(`/comments/${id}`,
  {
    method: "POST",
    headers: {'Content-Type':'application/json'},
  body: JSON.stringify({comment: content})
})
.then(response => response.json())
.then(data => {
console.log(data)
if(post){
  console.log(post)
  commentDiv = document.getElementById("comments")
  postID = commentDiv.getAttribute("data-post-id")
  loadComments(postID)
  commentDiv.style.display = "block"
}
})
.catch(error => console.log(error))
document.getElementById(`${id}comment`).value = "";
form.style.display = "none";
}


const displayComment = (element, post=null) =>{
 id = element.id;
 form = document.getElementById(`${id}form`);
 if (form.style.display === "none") {
 form.style.display = "block";
 if (post) {
  document.getElementById("comments").style.display = "none"
 }
 } else {
    form.style.display = "none"
    if (post) {
      commentDiv = document.getElementById("comments")
      commentDiv.style.display = "block"
     }
  }
} 
 function postLikes (id,bool) {
    fetch(`/like/${id}`,{
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({liked: bool})
    }) 
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log({Error: error}))
}

function loadComments (postID){
    fetch("/comments", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({post_id: postID})
    })
    .then(response => {
      if(response.status === 200){
        return response.json()
       } else {
         throw new Error("Bad request")
       }
    })
    .then(data => {
       Div =  document.getElementById("comments")
       Div.innerHTML = "";
       data.forEach(({owner,comment,date}) => {    
        Div.innerHTML +=`
        <div>
        <a href="/profile/${owner}">
        <p><strong>@${owner}</strong></p></a>
        <p>${comment}</p>
        <p class="date">${date}</p>
        </div>
        <hr>
        `

       })
    })
}


function profileDisplay (element){
  document.querySelectorAll(".nav-link").forEach((nav) => {
    nav.classList.remove("active")
  })
  document.querySelectorAll(".profileDIsplay").forEach((nav) => {
    nav.classList.add("displayNav")
  })
  element.classList.add("active")
  divID = element.getAttribute("data")

  document.getElementById(divID).classList.remove("displayNav")
}


const displayCommentLikes = (element) =>{
  id = element.id.replace("like","")
  form = document.getElementById(`${id}formlike`);
  if (form.style.display === "none") {
  form.style.display = "block";
  } else {
     form.style.display = "none"
   }
 } 

 const handleSubmitlikes = (event) => {
  event.preventDefault();
  id = event.target.id.replace("formlike","")
  content = document.getElementById(`${id}commentlike`).value;
  fetch(`/comments/${id}`,
  {
    method: "POST",
    headers: {'Content-Type':'application/json'},
  body: JSON.stringify({comment: content})
})
.then(response => response.json())
.then(data => {
console.log(data)
})
.catch(error => console.log(error))
document.getElementById(`${id}commentlike`).value = "";
form.style.display = "none";
}

const heartColorlikes = (element) => {
  const id = element.id
 
  const heart = document.getElementById(`${id}`);
  postID = id.replace("heartlike","");
  
  if(heart.getAttribute("fill") === "gray") {
    heart.setAttribute("fill","red");
    postLikes(postID,true)
    addLikes(`${postID}likex`,true)
  } else {
    postLikes(postID,false)
    addLikes(`${postID}likex`,false)
    heart.setAttribute("fill","gray")
    
  }
}

 function following(element,following=null){
  
      const id = element.id

    fetch(`/following/${id.replace("follower","")}`,{
      method: "POST"
    })
    .then(response =>{
      if (response.status === 200){
        return response.json()
      } else {
        throw new Error("Bad request")
      }
    })
    .then(data => {
      console.log(data)
      followingColor(id)
    })
    .catch(error => console.log(error))
}

function followingColor(id){
    const followButton = document.getElementById(`${id}`)

    console.log(followButton)
  if (followButton.style.backgroundColor === "azure"){
    followButton.style.backgroundColor = "rgb(100, 179, 185)";
    followButton.innerHTML = "Following"
  }else{
    followButton.style.backgroundColor = "azure";
    followButton.innerHTML = "Follow"
  }
}

function addLikes(id,isLike) {
 element = document.getElementById(id)
 console.log(id)
 const count = Number(element.innerHTML)
 if (isLike === true){
  element.innerHTML = count + 1;
 } else {
  element.innerHTML = count - 1
 }

 
}