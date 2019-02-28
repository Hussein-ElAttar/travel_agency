from places.models import Country, City, UserCityRate, UserCarRent, UserHotelReservation
from places.forms import UserCityRateForm, UserCarRentForm, HotelReservationForm
from blog.forms import CommentForm, PostForm
from blog.models import Post, Comment

class CityHandler:


    def __init__(self,request,countryName, cityName):
        self.request  = request
        self.country  = Country.objects.get(name = countryName)
        self.city     = City.objects.get(name = cityName, country = self.country)

        if request.method == 'POST':
            self.__handle_post()


    def __handle_post(self):
        request = self.request
        rate_form    = UserCityRateForm(request.POST)
        post_form    = PostForm(request.POST, prefix='post_form')
        comment_form = CommentForm(request.POST, prefix='comment_form')
        self.__create_post(post_form)
        self.__rate_city(rate_form)
        self.__create_comment(comment_form)


    def get_context(self):
        rate_form = self.__get_saved_user_rating_form()
        blogs     = self.__get_posts_with_comments()
        context = {
            "is_loggedin":self.request.user.is_authenticated,
            "country": self.country, 
            "city": self.city,
            "rate_form": rate_form,
            "blogs": blogs,
            "comment_form": CommentForm(prefix='comment_form'),
            "post": PostForm(prefix='post_form'),
        }
        return context



    def __get_saved_user_rating_form(self):
        if self.request.user.is_authenticated:
            try:
                rate_value  = UserCityRate.objects.get(
                    user    = self.request.user,
                    city    = self.city
                ).rate
                user_rating = {"rate": rate_value}
            except :
                user_rating = None
            finally:            
                return UserCityRateForm(user_rating)
        else:
            return None
 

    def __get_posts_with_comments(self):
        posts_with_comments = []
        try:
            posts = Post.objects.filter(city=self.city)
            for post in posts:
                comments = Comment.objects.filter(post=post)
                posts_with_comments.append(
                    {'post': post,'comments': comments}
                )
        except:
            pass
        return posts_with_comments


    def __rate_city(self, form):
        if form.is_valid():
            try:
                rate = form.cleaned_data.get('rate')
                UserCityRate.objects.create(
                    user = self.request.user, 
                    city = self.city, 
                    rate = rate
                )
            except:
                UserCityRate.objects.filter(
                    user = self.request.user, 
                    city = self.city 
                ).update(rate = rate)


    def __create_post(self, post_form):
        if post_form.is_valid():
            postText = post_form.cleaned_data.get('text')
            Post.objects.create(
                user = self.request.user,
                city = self.city,
                text = postText
            )

    
    def __create_comment(self, comment_form):
        if comment_form.is_valid():
            try:
                post = Post.objects.get(
                    id = self.request.POST.get('comment_post_id')
                )
                text = comment_form.cleaned_data.get('text')
                Comment.objects.create(
                    user = self.request.user,
                    post = post,
                    text = text
                )
            except:
                pass