from django.contrib import admin
from .models import Vendor, VendorReview, VendorDocument

class VendorDocumentInline(admin.TabularInline):
    model = VendorDocument
    extra = 1

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'status', 'is_featured')
    list_filter = ('status', 'is_featured')
    search_fields = ('company_name', 'user__email', 'registration_number')
    prepopulated_fields = {'slug': ('company_name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [VendorDocumentInline]
    fieldsets = (
        (None, {'fields': ('user', 'company_name', 'slug', 'description')}),
        ('Contact Information', {'fields': ('phone_number', 'email', 'website', 'address')}),
        ('Business Details', {'fields': ('registration_number', 'tax_number')}),
        ('Documents', {'fields': ('business_certificate', 'tax_certificate', 'insurance_certificate')}),
        ('Social Media', {'fields': ('facebook', 'instagram', 'twitter')}),
        ('Bank Details', {'fields': ('bank_name', 'bank_account_name', 'bank_account_number', 'bank_routing_number')}),
        ('Status', {'fields': ('status', 'is_featured', 'verification_notes')}),
    )

@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor', 'rating', 'is_verified')
    list_filter = ('rating', 'is_verified')
    search_fields = ('user__email', 'vendor__company_name', 'comment')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(VendorDocument)
class VendorDocumentAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'document_type', 'name', 'is_verified')
    list_filter = ('document_type', 'is_verified')
    search_fields = ('vendor__company_name', 'name', 'description')
    readonly_fields = ('uploaded_at', 'verified_at')
