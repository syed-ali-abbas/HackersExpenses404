console.log('working regsister');
const usernameField = document.querySelector("#username-field");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#email-field");
const emailfeedBackArea = document.querySelector(".email_invalid_feedback");
const userNameSuccessOutput = document.querySelector(".userNameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector(".password-field");
const submitBtn= document.querySelector('.submit-btn');


const handleToggleInput=(e)=>{
if(showPasswordToggle.textContent==="SHOW"){
    showPasswordToggle.textContent="HIDE";
    passwordField.setAttribute('type','password');
}else{
    showPasswordToggle.textContent="SHOW";
    passwordField.setAttribute('type','show');}}
showPasswordToggle.addEventListener("click",handleToggleInput);

// -------------------------Username Validation--------------------------------------

usernameField.addEventListener("keyup",(e)=>{
const usernameVal = e.target.value;
userNameSuccessOutput.style.display="block";
userNameSuccessOutput.style.display='none';
usernameField.classList.remove("is-invalid");
// submitBtn.disabled=false;
feedBackArea.style.display="none";
if(usernameVal.length>0){
fetch("/authentication/validate-username",{
body:JSON.stringify({username:usernameVal}),method:"POST",
})
.then((res)=>res.json())
.then((data)=>{
    console.log(data);
    
    userNameSuccessOutput.textContent=`Checking ${usernameVal}`;
    if(data.username_error){
        submitBtn.setAttribute("disabled","disabled");
        usernameField.classList.add("is-invalid");
        feedBackArea.style.display="block";
        feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
    }
    else{submitBtn.removeAttribute("disabled");}
});
}
});

// ------------------------------Email Validation---------------------------------------------
emailField.addEventListener("keyup",(e)=>{
    const emailVal = e.target.value;
    emailSuccessOutput.style.display='none';
    emailSuccessOutput.style.display="block";
    emailField.classList.remove("is-invalid");
    emailfeedBackArea.style.display="none";
    // submitBtn.disabled=false;
    if(emailVal.length>0){

        fetch("/authentication/validate-email",{
        body:JSON.stringify({email:emailVal}),method:"POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log(data);
        emailSuccessOutput.textContent=`Checking ${emailVal}`;
            if(data.email_error){
                submitBtn.setAttribute("disabled","disabled");
                emailField.classList.add("is-invalid");
                emailfeedBackArea.style.display="block";
                emailfeedBackArea.innerHTML=`<p>${data.email_error}</p>`;
    }
    else
    {
        submitBtn.removeAttribute("disabled");
        
}});

}});