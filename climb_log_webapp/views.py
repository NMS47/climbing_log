from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime
import smtplib
#For plotly charts
import pandas as pd
from plotly.offline import plot
import plotly.express as px

from datetime import datetime, timedelta
from plotly_calplot import calplot
import folium

from .models import ClimbEntry,  ClimbPlaces
from .forms import NewEntryForm, UpdateEntryForm, UserCreateForm, ContactForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


grades_list = [[['Color'],['verde', 'azul', 'amarillo', 'naranja', 'rojo', 'negro']],
               [['V'],['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15']],
              [['FR'],['5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b', '8b+', '8c','8c+']]
               ] 
# This is to asign a value to the grades
# grades_dict = {}
# for grade_list in grades_list:
#     category = grade_list[0][0]  # Get the category name
#     grades = grade_list[1]  # Get the list of grades
#     grades_dict[category] = {grade: i + 1 for i, grade in enumerate(grades)}
#-----------------------------------------
# grades_dict = [[['Color'],[{'verde': 1, 'azul': 2, 'amarillo': 3, 'naranja': 4, 'rojo': 5, 'negro': 6}]],
#                [['V'],[{'V0': 1, 'V1': 2, 'V2': 3, 'V3': 4, 'V4': 5, 'V5': 6, 'V6': 7, 'V7': 8, 'V8': 9, 'V9': 10, 'V10': 11, 'V11': 12, 'V12': 13, 'V13': 14, 'V14': 15, 'V15': 16}]],
#               [['FR'],[{'5': 1, '5+': 2, '6a': 3, '6a+': 4, '6b': 5, '6b+': 6, '6c': 7, '6c+': 8, '7a': 9, '7a+': 10, '7b': 11, '7b+': 12, '7c': 13, '8a': 14, '8a+': 15, '8b': 16, '8b+': 17, '8c': 18, '8c+': 19}]]
#                ] 
grades_dict={'verde': 1, 'azul': 2, 'amarillo': 3, 'naranja': 4, 'rojo': 5, 'negro': 6, 'V0': 1, 'V1': 2, 'V2': 3, 'V3': 4, 'V4': 5, 'V5': 6, 'V6': 7, 'V7': 8, 'V8': 9, 'V9': 10, 'V10': 11, 'V11': 12, 'V12': 13, 'V13': 14, 'V14': 15, 'V15': 16, '5': 1, '5+': 2, '6a': 3, '6a+': 4, '6b': 5, '6b+': 6, '6c': 7, '6c+': 8, '7a': 9, '7a+': 10, '7b': 11, '7b+': 12, '7c': 13, '8a': 14, '8a+': 15, '8b': 16, '8b+': 17, '8c': 18, '8c+': 19 }

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('entry-list')
    
class SignUpView(FormView):
    form_class = UserCreateForm
    template_name = 'registration/sign_up.html'
    
    def get_success_url(self):
        return reverse_lazy('successful-sign-up')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(SignUpView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('entry-list')
        
        return super(SignUpView, self).get(*args, **kwargs)

class HomeView(TemplateView):
    template_name = 'climb_log_webapp_ES/home.html'

class NewEntryView(LoginRequiredMixin, FormView):
    template_name = 'climb_log_webapp_ES/new_entry.html'
    form_class = NewEntryForm
    extra_context = {'multipitches': False,
                     'num_pitches': 1,
                    #  'ascent_type': 'not-specified',
                     'num_attempts': 1,
                     'date_today': datetime.today().strftime('%Y-%m-%d'),
                     'attempts': [i for i in range(1,9)],
                     'grades_list': grades_list
                                          }
    success_url =reverse_lazy('successful-new-entry')
    model = ClimbEntry

# This is to pass variables to the template 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = ClimbPlaces.objects.values_list('id','place_name')
        places_list = [[n[0],n[1]] for n in queryset.all()]
        context['places_list'] = places_list
        context['form_type'] = self.kwargs['form_type']
        print(context['form_type'])
        return context

# This is to add a username, grade_equivalent to the climbEntry, otherwise it is not saved to db
    def form_valid(self, form):
        form.instance.grade_equivalent = grades_dict.get(form.instance.grade)
        # form.instance.ascent_type = 'not-specified'
        number_of_entries = int(self.request.POST.get('multiple_entries','')) 
        form.instance.username = self.request.user
        instance = form.save(commit=False)
        for n in range(number_of_entries):
            instance.pk = None
            instance.save()
        return super().form_valid(form)
    

class SuccessfulSignUp(TemplateView):
    template_name = 'climb_log_webapp_ES/successful_sign_up.html' 


class SuccessfulNewEntry(LoginRequiredMixin, ListView):
    template_name = 'climb_log_webapp_ES/successful_new_entry.html'
    model = ClimbEntry
    context_object_name = 'entries'

    def get_queryset(self):
        user_entries = super().get_queryset()
        data = user_entries.filter(username=self.request.user)
        return data
    
class Profile(LoginRequiredMixin, ListView):
    template_name= 'climb_log_webapp_ES/profile.html'
    model = ClimbEntry
    allow_empty=False

    context_object_name = 'entries'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = context['entries'].filter(username_id=self.request.user.id)
        if not context['entries'].filter(username_id=self.request.user.id):
            print(context['entries'])
            return context

        today = datetime.now()
        formated_today= today.strftime("%Y-%m-%d")
        four_months_ago = today - timedelta(days=124)
        # one_ago = today - timedelta(days=365)
        # formated_ago = one_ago.strftime("%Y-%m-%d")
        # df_download = pd.DataFrame(context['entries'])
        # df_download.to_csv('home/nms/Downloads/')

        #-----------------------Heatmap calendar--------------------------------------
        df_calendar = pd.DataFrame(context['entries'].values('date_of_climb', 'num_pitches', 'num_attempts'))
        df_calendar["intensity"] = (((df_calendar['num_pitches']**2) + df_calendar['num_attempts'])/2).astype('int64')
        df_intensity = df_calendar.groupby('date_of_climb', as_index=False).sum()
        df_intensity['date_of_climb']= pd.to_datetime(df_intensity['date_of_climb'], format='%Y-%m-%d', errors='raise')
        df_intensity['date_of_climb'] = df_intensity['date_of_climb'].dt.strftime('%Y-%m-%d')

        starting_day_of_current_year = datetime.now().date().replace(month=1, day=1)
        idx = pd.date_range(starting_day_of_current_year, formated_today)
        #this is the code for exactly one year ago
        # idx = pd.date_range(formated_ago, formated_today)
        df_intensity.index = df_intensity['date_of_climb']
        df_intensity.index = pd.DatetimeIndex(df_intensity.index)
        df_intensity = df_intensity.reindex(idx, fill_value=0)
        df_intensity['date_of_climb'] = df_intensity.index

        fig_cal = calplot(
            df_intensity,
            x="date_of_climb",
            y="intensity",
            dark_theme=True,
            colorscale=[
    (0.00, "#4d4c4c"),   # Grey
    (0.20, "#f7a559"),  # Light Orange
    (0.40, "#f39742"),  # semi - Orange
    (0.40, "#eead35"),  # Orange
    (0.60, "#ff8c00"),  # Darker orange
    (0.80, "#ff7300"),  # Even Darker orange
    (1.00, "#ff4500")   # Dark orange
],
            years_title=True,
            gap=2,
            month_lines_width=4, 
            month_lines_color="#666464",
            name = 'pegues',
            showscale=True,
            space_between_plots= 0.1,
            start_month=int(four_months_ago.month),
            end_month=int(today.month))
        fig_cal.update_layout(margin=dict(l=6, r=6))
        cal_plot = plot(fig_cal, output_type='div',config={'scrollZoom': False, 'displayModeBar': False})
        context['calendar_plot'] = cal_plot
        #--------------------------------------------------------------------

        #--------------Styles chart----------------------------------
        styles_df = pd.DataFrame(context['entries'].values('climb_style', 'num_attempts'))
        g_df = styles_df.groupby(by=['climb_style'], as_index=False).sum()
        g_df.insert(0, 'Estilo', 'Estilo')
        
        fig = px.bar(g_df, x="num_attempts", y='Estilo', color="climb_style", orientation='h', text_auto=True,  color_discrete_sequence=["#2CA02C", "#9467BC", "#1F77B4",], hover_name='climb_style', hover_data={'Estilo':False, 'climb_style':False, 'num_attempts':False})
        fig.update_layout(paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', xaxis=dict(color='white'), yaxis=dict(color='white'), height=100, width=300, margin=dict(l=6, r=0, t=26, b=6), barmode='stack', yaxis_title=None, xaxis_title=None, legend_font_color='#F4F4F4', legend_font_size=8, legend_borderwidth=0, legend_title=None)
        fig.update_yaxes(showticklabels=True, visible=False)
        fig.update_traces(width=0.5, )
        styles_chart = plot(fig, output_type='div',config={'scrollZoom': False, 'displayModeBar': False})
        context['style_chart'] = styles_chart
        #--------------------------------------------------------------
        #-------------Records------------------------------------------
        df_records = pd.DataFrame(context['entries'].values('date_of_climb', 'climb_style', 'grade', 'grade_equivalent'))
        # This can be done grouping values by climb style, autodetecting trad if there is any.
        styles= ['sport','boulder']
        #--
        records = []
        for style in styles:
            try:
                style_record = df_records[df_records['climb_style'] == style]['grade_equivalent'].idxmax()
                r_grade = df_records.loc[style_record]['grade']
                r_date = df_records.loc[style_record]['date_of_climb']
            except ValueError:
                r_grade = "-"
                r_date = "-"
            finally:
                records.append((r_grade, r_date))
        context['records'] = records
        #--------------------------------------------------------------
        #Fav place-----------------------------------------------------
        fav_list = []
        df_place = pd.DataFrame(context['entries'].values('climb_style', 'place_name__place_name'))
        
        df_fav = df_place.groupby(['climb_style','place_name__place_name'], as_index=False).value_counts()
        for style in styles:
            try:   
                id = df_fav[df_fav['climb_style']==style]['count'].idxmax()
                style_fav = df_fav.loc[id].place_name__place_name
            except ValueError:
                style_fav = "-"
            finally:
                fav_list.append(style_fav)
        context['favorite_places'] = fav_list
        #-------------------------------------------------------------
        #Progression line---------------------------------------------
        # By creating a month column we can get an accurate monthly max climb grade, should check if there is a better way
        df_records['month'] = pd.DatetimeIndex(df_records['date_of_climb']).month
        df_prog = df_records.groupby(['month','climb_style'], as_index=False).max()
        print(df_prog)
        
        fig = px.line(df_prog, x='date_of_climb', y="grade_equivalent", color='climb_style', markers=True, color_discrete_sequence=["#2CA02C", "#9467BC", "#1F77B4",], hover_name='date_of_climb', hover_data={'climb_style':False, 'grade_equivalent':False, 'date_of_climb':False}, line_shape='spline')
        fig.update_layout(paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', 
                          xaxis=dict(color='white', tickangle=-45, griddash='dot', gridwidth=0.3, fixedrange=False, linecolor='white', gridcolor='#757575', linewidth=1.5, spikecolor='#232020', spikedash='solid', spikethickness=1, tickfont_family='Rubik', tickformat='%b',), 

                          yaxis=dict(color='white', gridcolor='#757575', griddash='dot', gridwidth=0.3, fixedrange=True, labelalias={1: '5', 1.5:' ', 2: '5+', 2.5:' ', 3: '6a',3.5:' ', 4:'6a+', 4.5:' ', 5:'6b', 5.5:' ', 6: '6b+',6.5:' ', 7: '6c', 7.5: ' ', 8: '6c+', 8.5:' ', 9: '7a',  9.5: ' ', 10: '7a+', 10.5: ' ',
                         11: '7b', 11.5: ' ', 12: '7b+', 12.5: ' ', 13: '7c', 13.5:' ', 14:'8a', 14.5: ' ', 15: '8a+', 15.5:' ', 16: '8b', 16.5:' ', 17:'8b+', 17.5: ' ', 18: '8c', 18.5:' ', 19:'8c+', 19.5:' '}, linecolor='#F4F4F4', linewidth=1.5, tickfont_family='Rubik'), height=225, margin=dict(l=6, r=0, t=26, b=6), yaxis_title=None, xaxis_title=None, legend_font_color='#F4F4F4', legend_font_size=8, legend_borderwidth=0, legend_title=None)
        fig.update_yaxes(ticklabelstep=1)
        prog_plot = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, config={'scrollZoom': False, 'displayModeBar': False})
        context['prog_plot'] = prog_plot

        #Climbs maps----------------------------------------
        # This is for eventually making a csv file in excel that is easier to add climbing places

        # places = Climb_places_from_csv.import_data(data = open('static/lugares_escalada.csv'))
        # print(places[0].name)
        # file =open('static/lugares_escalada.csv')
        # places_data = pd.read_csv(file)
        # ramos = places_data[places_data['name'] =='El Muro de Ramos']['coords'].values[0].split(',')
        # buca = places_data[places_data['name'] =='CABA Bucarelli']['coords'].values[0].split(',')
        # https://python-visualization.github.io/folium/modules.html all the params
        df_map = pd.DataFrame(context['entries'].values('place_name__place_name', 'place_name__place_coords', 'place_name__enviroment'))
        df_map.drop_duplicates(inplace=True)
        

        #For setting the map coordinates and initial zoom level
        figure = folium.Figure()
        m = folium.Map(
            location=[-38.0000, -63.0000],
            zoom_start=4,
            max_zoom=12,
        )
        m.default_css=[('leaflet_css', 'https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css'), ('awesome_markers_font_css', 'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css'), ('awesome_markers_css', 'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css'), ('awesome_rotate_css', 'https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css')]
        m.add_to(figure)
        #For making the pins in the map:
        for index, row in df_map.iterrows():
            pin_color = 'lightblue'
            if row[2] == 'artificial':
                pin_color = 'lightred'
            folium.Marker(
            location=[float(row[1].split(',')[0]), float(row[1].split(',')[1])],
            popup=row[0],
            icon=folium.Icon(color=pin_color),
        ).add_to(m)
        figure.render()
        context["map"] = figure
        return context

    
class EntryList(LoginRequiredMixin, ListView):
    template_name= 'climb_log_webapp_ES/entry_list.html'
    model = ClimbEntry
    paginate_by = 15
    context_object_name = 'entries'
    
    #This is the way of filtering the db when using paginator
    def get_queryset(self):
        return ClimbEntry.objects.filter(username_id=self.request.user.id).order_by('-date_of_climb')
  
    
class EntryDetail(LoginRequiredMixin, DetailView):
    template_name= 'climb_log_webapp_ES/entry_detail.html'
    model = ClimbEntry
    context_object_name = 'entry'


class EntryUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'climb_log_webapp_ES/entry_update.html'
    model = ClimbEntry
    # Created a form class to exclude the username field
    form_class = UpdateEntryForm
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')


class EntryDelete(LoginRequiredMixin, DeleteView):
    template_name = 'climb_log_webapp_ES/entry_confirm_delete.html'
    model = ClimbEntry
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')
 
    
class ContactPage(FormView):
    template_name = 'climb_log_webapp_ES/contact.html' 
    form_class = ContactForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form: Any):
        form.send_email(form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'])
        return super().form_valid(form)