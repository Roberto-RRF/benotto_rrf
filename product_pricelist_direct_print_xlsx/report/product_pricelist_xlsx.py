# Copyright 2021 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class ProductPricelistXlsx(models.AbstractModel):
    _name = "report.product_pricelist_direct_print_xlsx.report"
    _inherit = "report.report_xlsx.abstract"
    _description = "Abstract model to export as xlsx the product pricelist"

    def _get_lang(self, user_id, lang_code=False):
        if not lang_code:
            lang_code = self.env["res.users"].browse(user_id).lang
        return self.env["res.lang"]._lang_get(lang_code)

    def _create_product_pricelist_sheet(self, workbook, book, pricelist):
        title_format = workbook.add_format(
            {"bold": 1, "border": 1, "align": "left", "valign": "vjustify"}
        )
        header_format = workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vjustify",
                "fg_color": "#F2F2F2",
            }
        )
        lang = self._get_lang(book.create_uid.id, lang_code=book.lang)
        date_format = lang.date_format.replace("%d", "dd")
        date_format = date_format.replace("%m", "mm")
        date_format = date_format.replace("%Y", "YYYY")
        date_format = date_format.replace("/", "-")
        date_format = workbook.add_format({"num_format": date_format})

        sheet = workbook.add_worksheet(_("PRODUCTS"))
        sheet.set_column("A:A", 25)  # Category
        sheet.set_column("B:B", 20)  # Reference
        sheet.set_column("C:C", 45)  # Name
        sheet.set_column("D:D", 15)  # Cost Price
        sheet.set_column("E:E", 15)  # Sale Price
        sheet.set_column("F:F", 15)  # List Price
        sheet.set_column("G:G", 15)  # UoM

        # Title row (like your "Nombre de la lista de precios", "Divisa", "Fecha")
        sheet.write("A1", _("Price List Name:"), title_format)
        if book.show_pricelist_name:
            sheet.write("A2", pricelist.name)
        else:
            sheet.write("A2", _("Special Pricelist"))

        sheet.write("B1", _("Currency:"), title_format)
        sheet.write("B2", pricelist.currency_id.name)

        sheet.write("D1", _("Date:"), title_format)
        sheet.write("D2", book.date, date_format)

        # If you want partner name in row 4
        if book.partner_id:
            sheet.write(4, 0, book.partner_id.name, header_format)
        elif book.partner_ids:
            sheet.write(4, 0, book.partner_ids[0].name, header_format)

        # Header row (row 5)
        # You can rename them to Spanish, or keep them in English. Example in Spanish:
        row_header = 5
        sheet.write(row_header, 0, _("Categoría"), header_format)
        sheet.write(row_header, 1, _("Referencia"), header_format)
        sheet.write(row_header, 2, _("Nombre"), header_format)
        sheet.write(row_header, 3, _("Precio de costo"), header_format)
        sheet.write(row_header, 4, _("Precio de venta"), header_format)
        sheet.write(row_header, 5, _("Lista de Precios"), header_format)
        sheet.write(row_header, 6, _("UoM"), header_format)

        return sheet

    def _add_extra_header(self, sheet, book, next_col, header_format):
        return next_col

    def _fill_data(self, workbook, sheet, book, pricelist):
        bold_format = workbook.add_format({"bold": 1})
        decimal_format = workbook.add_format({"num_format": "0.00"})
        decimal_bold_format = workbook.add_format({"num_format": "0.00", "bold": 1})

        row = 6  # Data starts at row 6
        for group in book.get_groups_to_print():

            # if book.breakage_per_category:
            #     sheet.write(row, 0, group["group_name"], bold_format)
            #     row += 1

            for product in group["products"]:
                # Column 0: Category/Group
                sheet.write(row, 0, group["group_name"] or "",)

                # Column 1: Reference (product.default_code)
                sheet.write(row, 1, product.default_code or "")

                # Column 2: Product Name
                sheet.write(row, 2, product.name)

                # Column 3: Cost Price
                if book.show_standard_price:
                    sheet.write(row, 3, product.standard_price, decimal_format)
                else:
                    sheet.write(row, 3, "")  # or skip entirely

                # Column 4: Sale Price
                if book.show_sale_price:
                    sheet.write(row, 4, product.list_price, decimal_format)
                else:
                    sheet.write(row, 4, "")

                # Column 5: Computed Price
                sheet.write(
                    row,
                    5,
                    book.with_context(product=product).product_price,
                    decimal_bold_format,
                )

                # Column 6: UoM
                if book.show_product_uom:
                    sheet.write(row, 6, product.uom_id.name or "", bold_format)
                else:
                    sheet.write(row, 6, "")

                row += 1

        # If you have a summary at the end
        if book.summary:
            sheet.write(row, 0, _("Summary:"), bold_format)
            sheet.write(row + 1, 0, book.summary)
        return sheet
    
    def _add_extra_info(self, sheet, book, product, row, next_col, **kw):
        return next_col

    def generate_xlsx_report(self, workbook, data, objects):
        book = objects[0].with_context(
            lang=objects[0].lang
            or self.env["res.users"].browse(objects[0].create_uid.id).lang
        )
        self = self.with_context(
            lang=book.lang or self.env["res.users"].browse(book.create_uid.id).lang
        )
        pricelist = book.get_pricelist_to_print()
        sheet = self._create_product_pricelist_sheet(workbook, book, pricelist)
        sheet = self._fill_data(workbook, sheet, book, pricelist)
