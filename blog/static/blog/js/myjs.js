    $(function() {
        $(window).bind('scroll', function() {
            if ($(document).scrollTop() > 500) {
                $(".fixed-action-btn").show();
            } else {
                $(".fixed-action-btn").hide();
            }
        })
        $(".fixed-action-btn").click(function() {
            $('body,html').animate({ scrollTop: 0 }, 1000);
        })
    })
    $(document).ready(function() {
        $('.sidenav').sidenav();
    });
    $(document).ready(function() {
        $('.carousel').carousel();
    });
    $(document).ready(function() {
        $('.fixed-action-btn').floatingActionButton();
    });
    $('.fixed-action-btn').floatingActionButton();
    $(document).ready(function() {
        $('.collapsible').collapsible();
    });
    $(document).ready(function(){
	$("h2,h3,h4").addClass("section scrollspy");
	});
    $(document).ready(function(){
        $("div.toc ul:first").addClass("section table-of-contents fixed");
	});
    $(document).ready(function() {
        $('.scrollspy').scrollSpy();
    });
