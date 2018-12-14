function get_movies() {
    $.get('/api/movie/hot_movies', function (data) {
        var movies_data = JSON.parse(data);
        var movies = movies_data.data;
        for (i=0; i<movies.length; i++) {
            var $li = $('<li data-target="#myCarousel" data-slide-to="' + i + '"></li>');
            var $div = $('<div class="item"></div>');
            if (i == 0) {
                $li.addClass("active");
                $div.addClass("active");
            }
            h = '<a href="'+'movie/'+movies[i].id+'"><img src="' + movies[i].img_url + '"></a><div class="carousel-caption">' + movies[i].name + '</div>';
            $div.html(h);
            $(".carousel-indicators").append($li);
            $(".carousel-inner").append($div);

            // $("#movie-list").append($('<a href="movie/'+movies[i].id+'" class="list-group-item">'+movies[i].name+'</a>'))
        }
    });
}

$(function () {
    get_movies();
});
