    function getAllUsers() {
        $.ajax(
            {
                url: '/fetchUsers/',
                type: "post",
                data: {"username": document.getElementById('current_user_lgin').value},
                success: function (responseData) {
                    if (responseData['result']) {

                        for (var us=0;us<responseData['result'].length;us++)
                        {
                            var inp = document.createElement("input");
                            inp.setAttribute("type", "hidden");
                            inp.setAttribute("disabled", "true");
                            inp.setAttribute("class", "all_users");
                            inp.setAttribute("value", responseData['result'][us]);
                            document.body.appendChild(inp);
                        }

                        // if (responseData['result'].include())
                    } else {

                    }
                },
                failure: function (res) {
                    alert('something went wrong');
                }
            }
        )

    }
