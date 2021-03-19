console.log('working regsister');
const usernameField = document.querySelector("#username-field");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#email-field");
const emailfeedBackArea = document.querySelector(".email_invalid_feedback");
const userNameSuccessOutput = document.querySelector(".userNameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");



// -------------------------Username Validation--------------------------------------
usernameField.addEventListener("keyup",(e)=>{
const usernameVal = e.target.value;
userNameSuccessOutput.style.display="block";
userNameSuccessOutput.textContent=`Checking ${usernameVal}`;
usernameField.classList.remove("is-invalid");
feedBackArea.style.display="none";
if(usernameVal.length>0){
fetch("/authentication/validate-username",{
body:JSON.stringify({username:usernameVal}),method:"POST",
})
.then((res)=>res.json())
.then((data)=>{
    console.log(data);
    userNameSuccessOutput.style.display='none';
    if(data.username_error){
        usernameField.classList.add("is-invalid");
        feedBackArea.style.display="block";
        feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
    }
});
}
});
// ------------------------------Email Validation---------------------------------------------
emailField.addEventListener("keyup",(e)=>{
    const emailVal = e.target.value;
    emailSuccessOutput.textContent=`Checking ${emailVal}`;
    emailSuccessOutput.style.display="block";
    emailField.classList.remove("is-invalid");
    emailfeedBackArea.style.display="none";
    if(emailVal.length>0){
        fetch("/authentication/validate-email",{
        body:JSON.stringify({email:emailVal}),method:"POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log(data);
        emailSuccessOutput.style.display='none';
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailfeedBackArea.style.display="block";
                emailfeedBackArea.innerHTML=`<p>${data.email_error}</p>`;
    }
    });
    }
    });