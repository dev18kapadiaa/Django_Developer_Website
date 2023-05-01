
 // Get Search Form and Page Links
let searchForm = document.getElementById('searchForm')
let pageLink = document.getElementsByClassName('page-link')

 // Ensure Search Form Exists
 if(searchForm){
     for(let i=0; pageLink.length > i; i++){
         pageLink[i].addEventListener('click', function (e) {
             e.preventDefault()

             // Get data attributes
             let page = this.dataset.page

             // Add Hidden Search Input to Form
             searchForm.innerHTML += `<input value=${page} name="page" hidden />`

             // Submit Form
             searchForm.submit()
         })
     }
 }