from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View 
from django import forms 
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page for an online store.", 
            "author": "Developed by: Alejandra Suarez", 
        }) 
        return context 

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

 
class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price": 2500},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 1650},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 500},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 87} 
    ] 
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        if not id.isdigit() or int(id) < 1 or int(id) > len(Product.products):
            return HttpResponseRedirect(reverse('home'))

        product = Product.products[int(id)-1]
        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product
        }
        return render(request, self.template_name, viewData)
 
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return price 
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid():
            return render(request, 'products/product_created.html', 
            { "title": "Product created"}) 
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)