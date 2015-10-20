function getChecked()
{
    candidates = document.getElementsByName("candidate")
    for (i in candidates)
    {
        if(candidates[i].checked)
        {
            return candidates[i].id
        }
    }
    return ''
}

function vote(caller)
{
    document.getElementById("voted").value = caller.id
}