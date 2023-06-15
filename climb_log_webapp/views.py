from django.shortcuts import render, redirect
from datetime import datetime
#For plotly charts
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from datetime import datetime, timedelta
from plotly_calplot import calplot

import requests
from .models import User, Climb_entry
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import NewEntryForm, UpdateEntryForm, UserCreateForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin



grades_list = [[['Color'],['verde', 'azul', 'amarillo', 'naranja', 'rojo', 'negro']],
               [['V'],['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15']],
              [['FR'],['5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b', '8b+', '8c','8c+']]
               ] 

# PIXELA_TOKEN = "the_climbing_log"
# PIXELA_URL = 'https://pixe.la'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # self.request.session['pixela_username'] = f"{self.request.user}climbinglog".lower()
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
            # self.request.session['pixela_username'] = f"{self.request.user}climbinglog".lower()
            # response = requests.post(f'{PIXELA_URL}/v1/users', json={
            #     "token":PIXELA_TOKEN, 
            #     "username":self.request.session['pixela_username'], 
            #     "agreeTermsOfService":"yes", 
            #     "notMinor":"yes",
            #      })
            # print(response.text)

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
    success_url =reverse_lazy('successful-new-entry')
    model = Climb_entry

# This is to pass variables to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date_today"] = datetime.today().strftime('%Y-%m-%d')
        context["attempts"] = [i for i in range(1,9)]
        context["grades_list"] = grades_list
        return context

# This is to add a username to the climb_entry, otherwise it is not saved to db
    def form_valid(self, form):
        number_of_entries = int(self.request.POST.get('multiple_entries',''))
        form.instance.username = self.request.user
        instance = form.save(commit=False)
        for n in range(number_of_entries):
            instance.pk = None
            instance.save()

    # Second part is to save data in pixela
            # pixela_user = self.request.session['pixela_username']
            # graph_id = f'climblog{str(self.request.user.id)}'
            # date = (form.instance.date_of_climb).strftime('%Y%m%d')
            # #This is a made-up coeficient so that a multipitch is worth more than an attempt in the
            # #intensity of climb
            # total_quatity = round((form.instance.num_pitches*2 + form.instance.num_attempts)/3)
            # #This while loop is here because pixela reject 25% of requests for non-supporter
            # while True:
            #     response = requests.post(f'{PIXELA_URL}/v1/users/{pixela_user}/graphs/{graph_id}',
            #                                 json={
            #                                     "date":f"{date}",
            #                                     "quantity": f"{total_quatity}",
            #                                     # "optionalData":f"{form.instance.num_attempts}",
            #                                 },
            #                                 headers={'X-USER-TOKEN': PIXELA_TOKEN})
            #     print(response.text)
            #     response_data = response.json()
            #     if response_data['isSuccess']:
            #         break
            # print('entry saved')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))



class SuccessfulSignUp(TemplateView):
    template_name = 'climb_log_webapp_ES/successful_sign_up.html'

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         pixela_user = self.request.session['pixela_username']
            
    #         response = requests.post(f'{PIXELA_URL}/v1/users/{pixela_user}/graphs', 
    #             json={
    #                 "id":f"climblog{str(self.request.user.id)}",
    #                 "name":pixela_user,
    #                 "unit":"climbs",
    #                 "type":"int",
    #                 "color":"shibafu",
    #                 "timezone":"America/Argentina/Buenos_Aires"
    #             },
    #             headers={'X-USER-TOKEN': PIXELA_TOKEN},)
    #         print(response.text)
    #     return super().get(*args, **kwargs)    


class SuccessfulNewEntry(LoginRequiredMixin, ListView):
    template_name = 'climb_log_webapp_ES/successful_new_entry.html'
    model = Climb_entry
    context_object_name = 'entries'

    def get_queryset(self):
        user_entries = super().get_queryset()
        data = user_entries.filter(username=self.request.user)
        return data
    
class Profile(LoginRequiredMixin, ListView):
    template_name= 'climb_log_webapp_ES/profile.html'
    model = Climb_entry
    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pixela_user = self.request.session['pixela_username']
        # graph_id = f'climblog{str(self.request.user.id)}'
        # context['pixela'] = f'{PIXELA_URL}/v1/users/{pixela_user}/graphs/{graph_id}'
        context['entries'] = context['entries'].filter(username_id=self.request.user.id)

        # df_download = pd.DataFrame(context['entries'].values())
        # df_download.to_csv('pegues.csv')

        simple_charts = []
        col_names = ['enviroment','climb_style', 'grade', 'climber_position', 'ascent_type']
        today = datetime.now()
        formated_today= today.strftime("%Y-%m-%d")
        one_ago = today - timedelta(days=365)
        formated_ago = one_ago.strftime("%Y-%m-%d")
        # df_download = pd.DataFrame(context['entries'])
        # df_download.to_csv('home/nms/Downloads/')

        #Heatmap calendar
        df_calendar = pd.DataFrame(context['entries'].values('date_of_climb','num_pitches', 'num_attempts'))
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
            start_month=2,
            end_month=6)
        cal_plot = plot(fig_cal, output_type='div')
        context['calendar_plot'] = cal_plot

        df_grades = pd.DataFrame(context['entries'].values('enviroment', 'ascent_type', 'num_attempts'))
        clean_df = df_grades.groupby(by=['enviroment','ascent_type'], as_index=False).sum()

        fig = px.bar(clean_df, x='enviroment', 
                     y='num_attempts', 
                     color='ascent_type',
                     color_continuous_scale=px.colors.sequential.Viridis
                     )
        fig.update_layout(paper_bgcolor = 'rgba(0, 0, 0, 0)', 
                          plot_bgcolor = 'rgba(0, 0, 0, 0)', 
                          xaxis=dict(color='white'), yaxis=dict(color='white'), 
                          height=300, width=250, 
                          margin=dict(l=20, r=0, t=26, b=6),
                          legend=dict(font=dict(
                                        family="Arial",
                                        size=10,
                                        color="white")),
                          
                          )
        # fig.add_trace(bar)
        
        effectiveness_plot = plot(fig, output_type='div',)
        context['effectiveness_plot'] = effectiveness_plot
        simple_charts.append(context['effectiveness_plot'])

        # Pie Chart of climbing style
        data= context['entries'].values('climb_style', 'num_attempts')
        df_style = pd.DataFrame(data)

        fig = px.pie(df_style, values='num_attempts', names='climb_style', title='Tipo de Escalada', color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_layout(paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)',  xaxis=dict(color='white'), yaxis=dict(color='white'), height=400, width=400, margin=dict(l=6, r=0, t=26, b=6), )
        style_plot = plot(fig, output_type='div',)
        context['style_plot'] = style_plot
        simple_charts.append(context['style_plot'])

        # Bar charts of varios data
        col_names = ['enviroment','climb_style', 'grade', 'climber_position', 'ascent_type']
        for column_name in col_names:
            df = pd.DataFrame(context['entries'].values(column_name))
            value_count = df.value_counts()

            fig = go.Figure()
            bar = go.Bar(x=value_count.index.get_level_values(0), y=value_count.values, )
            fig.update_layout(showlegend=False, paper_bgcolor = 'rgba(0, 0, 0, 0)', plot_bgcolor = 'rgba(0, 0, 0, 0)', title=column_name.capitalize(),  xaxis=dict(color='white'), yaxis=dict(color='white'), height=200, width=200, margin=dict(l=6, r=0, t=26, b=6), )
            fig.add_trace(bar)
            fig.update_traces(marker_color=px.colors.qualitative.Prism)
            column_plot = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
            
            simple_charts.append(column_plot)
            context['columns_plots'] = simple_charts


        return context

    
class EntryList(LoginRequiredMixin, ListView):
    template_name= 'climb_log_webapp_ES/entry_list.html'
    model = Climb_entry
    paginate_by = 15
    context_object_name = 'entries'
    
    #This is the way of filtering the db when using paginator
    def get_queryset(self):
        return Climb_entry.objects.filter(username_id=self.request.user.id).order_by('-date_of_climb')
    
class EntryDetail(LoginRequiredMixin, DetailView):
    template_name= 'climb_log_webapp_ES/entry_detail.html'
    model = Climb_entry
    context_object_name = 'entry'

class EntryUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'climb_log_webapp_ES/entry_update.html'
    model = Climb_entry
    # Created a form class to exclude the username field
    form_class = UpdateEntryForm
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')

class EntryDelete(LoginRequiredMixin, DeleteView):
    template_name = 'climb_log_webapp_ES/entry_confirm_delete.html'
    model = Climb_entry
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)