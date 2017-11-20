from CholitoProject.userManager import get_user_index
from CholitoProject.fusioncharts import FusionCharts

from complaint.models import Complaint, AnimalType
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.views import View
import datetime

from municipality.forms import graphForm


class IndexView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_complaints_main.html'
    context = {}

    def getComplaintStats(self, complaints):
        stats_complaint = {}
        status_parser = dict(Complaint().COMPLAINT_STATUS)

        for key, value in status_parser.items():
            stats_complaint[value] = 0

        for complaint in list(complaints):
            temp_status = status_parser.get(complaint.status)
            stats_complaint[temp_status] += 1

        return stats_complaint

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        complaints = Complaint.objects.filter(
            municipality=user.municipality)

        self.context['complaints'] = complaints
        self.context['c_user'] = user
        self.context['stats'] = self.getComplaintStats(complaints)
        return render(request, self.template_name, context=self.context)


class StatisticsView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'
    template_name = 'muni_statistics.html'
    context = {}

    def graphByDate(self, request, id):
        user = get_user_index(request.user)

        today = datetime.datetime.now()
        timeframe = {'0': make_aware(today - datetime.timedelta(days=7)),
                     '1': make_aware(today - datetime.timedelta(days=30)),
                     '2': make_aware(today - datetime.timedelta(days=90)),
                     '3': make_aware(today - datetime.timedelta(days=180)),
                     '4': make_aware(today - datetime.timedelta(days=365))}
        captionTranslate = {
            '0': 'la ultima semana',
            '1': 'el ultimo mes',
            '2': 'el ultimo trimestre',
            '3': 'los ultimos seis meses',
            '4': 'el ultimo año',
        }
        fromDate = timeframe[id]

        data = Complaint.objects.filter(datetime__gte=fromDate)
        dataSource = {}
        dataSource['chart'] = {
            "caption": "Denuncias recibidas en " + captionTranslate[id],
            "subCaption": user.municipality.name,
            "xAxisName":"Estado de denuncias",
            "yAxisNAme":"Cantidad",
            "showPercentValues": "1",
            "bgColor": "#FFFFFF",
            "theme": "fint"
        }
        dataSource['data'] = []

        for (id,complaintType) in Complaint.COMPLAINT_STATUS:
            temp = {}
            temp['label'] = complaintType
            temp['value'] = data.filter(status=id).count()
            dataSource['data'].append(temp)
        graph = FusionCharts("column2D", "ex2", "100%", "100%", "chart-2", "json", dataSource)
        return graph

    def graphByType(self,request):
        user = get_user_index(request.user)
        # Grafico 1
        dataSource = {}
        dataSource['chart'] = {
            "caption": "Denuncias recibidas hasta el momento",
            "subCaption": user.municipality.name,
            "showPercentValues": "1",
            "bgColor": "#FFFFFF",
            #"pieRadius":"80",
            "theme": "zune"
        }
        dataSource['data'] = []
        complaints = Complaint.objects.filter(municipality=user.municipality)
        complaintTypes = Complaint.COMPLAINT_OPTIONS
        for (id,type) in complaintTypes:
            data = {}
            data['label'] = type
            data['value'] = complaints.filter(case=id).count()
            dataSource['data'].append(data)
        return FusionCharts("pie2D", "ex1", "100%", "100%", "chart-1", "json", dataSource)

    def get(self, request, **kwargs):
        user = get_user_index(request.user)
        # Grafico 1
        graph1 = self.graphByType(request)

        # grafico 2
        graph2 = self.graphByDate(request, '0')
        self.context['c_user'] = user
        self.context['output'] = graph1.render()
        self.context['output2'] = graph2.render()
        self.context['form'] = graphForm()
        return render(request, self.template_name, context=self.context)

    def post(self,request,**kwargs):
        user = get_user_index(request.user)
        form = graphForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['periodo']
            # Grafico 1
            graph1 = self.graphByType(request)

            # grafico 2
            graph2 = self.graphByDate(request, selected_option)
            self.context['c_user'] = user
            self.context['output'] = graph1.render()
            self.context['output2'] = graph2.render()
            self.context['form'] = graphForm(initial={'periodo':selected_option})
            return render(request, self.template_name, context=self.context)


class UserDetail(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'municipality.municipality_user_access'

    def post(self, request, **kwargs):
        c_user = get_user_index(request.user)
        if 'avatar' in request.FILES:
            c_user.municipality.avatar = request.FILES['avatar']
            c_user.municipality.save()
        return redirect('/')
