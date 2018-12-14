$(function () {
        var cinemas;

        function render_table(sechedules, source) {
            let table;
            switch (source) {
                case "糯米":
                    table = $("#detail1");
                    break;
                case "时光":
                    table = $("#detail2");
                    break;
            }

            if (schedules.today) {
                if (source == "糯米") {
                    $("#date").append($('<li><a href="#" date="today">今天</a></li>'));
                }
                table.html('');
                table.append($('<tr><th>开场时间</th><th>结束时间</th><th>类型</th><th>厅位</th><th>价格</th></tr>'));
                for (i = 0; i < schedules.today.length; i++) {
                    if (schedules.today[i].source == source) {
                        var $tr = $('<tr><td>' + schedules.today[i].start_time + '</td><td>' + schedules.today[i].end_time
                            + '</td><td>' + schedules.today[i].language + '</td><td>' + schedules.today[i].hall
                            + '</td><td>' + schedules.today[i].price + '</td></tr>');
                        table.append($tr)
                    }
                }
            }
            if (schedules.tomorrow && source == "糯米") {
                $("#date").append($('<li><a href="#" date="tomorrow">明天</a></li>'))
            }
            if (schedules.aftertomorrow && source == "糯米") {
                $("#date").append($('<li><a href="#" date="aftertomorrow">后天</a></li>'))
            }

            $("#date a").click(function () {
                var date_str = $(this).text();
                $("#dropdownMenu3").text(date_str);
                if (date_str == "今天") {
                    table.html('');
                    table.append($('<tr><th>开场时间</th><th>结束时间</th><th>类型</th><th>厅位</th><th>价格</th></tr>'));
                    for (i = 0; i < schedules.today.length; i++) {
                        if (schedules.today[i].source == source) {
                            var $tr = $('<tr><td>' + schedules.today[i].start_time + '</td><td>' + schedules.today[i].end_time
                                + '</td><td>' + schedules.today[i].language + '</td><td>' + schedules.today[i].hall
                                + '</td><td>' + schedules.today[i].price + '</td></tr>');
                            table.append($tr)
                        }
                    }
                }
                else if (date_str == '明天') {
                    table.html('');
                    table.append($('<tr><th>开场时间</th><th>结束时间</th><th>类型</th><th>厅位</th><th>价格</th></tr>'));
                    for (i = 0; i < schedules.tomorrow.length; i++) {
                        if (schedules.tomorrow[i].source == source) {
                            var $tr = $('<tr><td>' + schedules.tomorrow[i].start_time + '</td><td>' + schedules.tomorrow[i].end_time
                                + '</td><td>' + schedules.tomorrow[i].language + '</td><td>' + schedules.tomorrow[i].hall
                                + '</td><td>' + schedules.tomorrow[i].price + '</td></tr>');
                            table.append($tr)
                        }
                    }
                }
                else if (date_str == '后天') {
                    table.html('');
                    table.append($('<tr><th>开场时间</th><th>结束时间</th><th>类型</th><th>厅位</th><th>价格</th></tr>'));
                    for (i = 0; i < schedules.aftertomorrow.length; i++) {
                        if (schedules.aftertomorrow[i].source == source) {
                            var $tr = $('<tr><td>' + schedules.aftertomorrow[i].start_time + '</td><td>' + schedules.aftertomorrow[i].end_time
                                + '</td><td>' + schedules.aftertomorrow[i].language + '</td><td>' + schedules.aftertomorrow[i].hall
                                + '</td><td>' + schedules.aftertomorrow[i].price + '</td></tr>');
                            table.append($tr)
                        }
                    }
                }
            })
        }

        $("#schedule-result").css({"display": "none"});
        $("#date-selector").css({"display": "none"});
        $.get('/api/movie/cinema', function (data) {
            cinemas = JSON.parse(data).data;

        });
        select_cinema = function select(event) {
            $('#dropdownMenu2').text(event.target.innerHTML);
            $('#dropdownMenu3').text('今天');
            c_id = event.target.getAttribute('c_id');
            url = window.location.href;
            m_id = /movie\/(\d+)/.exec(url)[1];

            $.get('/api/movie/schedule', {'c_id': c_id, 'm_id': m_id}, function (data) {
                schedules = JSON.parse(data).data;
                if (schedules.today || schedules.tomorrow || schedules.aftertomorrow) {
                    // console.log(schedules);
                    $("#date-selector").css({"display": "inline-block"});
                    $("#schedule-result").css({"display": "block"});
                    $("#date").html('');

                    render_table(schedules, "糯米");
                    render_table(schedules, "时光");

                }
            })
        };


        $("#location a").click(function () {
            var location = $(this).text();
            $("#dropdownMenu1").text(location);
            $("#dropdownMenu2").html('选择电影院<span class="caret"></span>');
            $("#dropdownMenu3").text("今天");
            var cinema_list = cinemas[location];
            $("#cinema").html('');
            // console.log(cinema_list)
            for (i = 0; i < cinema_list.length; i++) {
                var $li = $('<li><a href="#" c_id="' + cinema_list[i].id + '" onclick="select_cinema(event)">' + cinema_list[i].name + '</a></li>');
                $('#cinema').append($li)
            }
        });

    }
);


