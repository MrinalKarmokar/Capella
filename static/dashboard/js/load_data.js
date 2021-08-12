console.log('hello world!')
let visible = 1

$.ajax({
    type: 'GET',
    url: `/dashboard/customers-json/${visible}/`,
    success: function(response){
        console.log(response.data)
        const data = response.data
        data.map(data=>{
            console.log(data.id)
        })
    },
    error: function(error){
        console.log(error)
    }
})