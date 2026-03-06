# Package Label with Customer (Odoo 17)

This module enhances Odoo 17 stock package labels (ZPL) by linking each package to its related delivery picking and printing the customer information directly on the label.[file:1][file:3]

The goal is to improve traceability in the warehouse: when you see a label on a box, you can immediately identify which customer and which transfer it belongs to.[file:1][file:3]

---

## Features

- Adds a computed `picking_id` field on `stock.quant.package` that stores the latest related transfer (`stock.picking`) for the package.[file:3]  
- Adds a computed `partner_id` field on `stock.quant.package` that stores the customer (`res.partner`) of that transfer.[file:3]  
- Updates the ZPL package label report so that customer details from `partner_id` are printed on the label (for example, customer name and address, depending on how you adjust the template).[file:1]  
- Works on top of the standard **Inventory** (`stock`) and **Delivery** (`delivery`) applications in Odoo 17.[file:1]  

---

## Data model and fields

This module does not create new models; it extends the existing `stock.quant.package` model.[file:3]

The following fields are added:

- `picking_id`  
  - Type: Many2one → `stock.picking`.[file:3]  
  - Purpose: Keeps a direct link from a package to the most recent transfer that used this package (either as `result_package_id` or `package_id`).[file:3]  
  - Computed: Value is set automatically by the compute method `_compute_partner_id` (read‑only by default in code).[file:3]  

- `partner_id`  
  - Type: Many2one → `res.partner`.[file:3]  
  - Purpose: Stores the customer of the transfer stored in `picking_id`, so that the package always “knows” which customer it is going to.[file:3]  
  - Computed: Also filled by `_compute_partner_id` (read‑only by default in code).[file:3]  

### How the compute method works

The compute method `_compute_partner_id` runs for each package and does the following:[file:3]

1. Searches `stock.move.line` for the latest line related to this package, matching either:  
   - `result_package_id = package.id`, or  
   - `package_id = package.id`.[file:3]  
2. Orders the move lines by `create_date` descending and takes only the first one (the newest record).[file:3]  
3. If a `picking_id` exists on that move line:  
   - Sets `package.picking_id` to that picking.[file:3]  
   - Sets `package.partner_id` to `picking.partner_id` (the customer of the transfer).[file:3]  
4. If no matching move line or picking is found:  
   - Sets both `package.picking_id` and `package.partner_id` to `False`.[file:3]  

This logic ensures that each package is automatically linked to the latest delivery operation and its customer, without manual input.[file:3]

---

## Label report (ZPL)

The module modifies the ZPL label report template used for printing package labels so that it can show customer information.[file:1]

- The report definition is provided in `views/package_label_report.xml`.[file:1]  
- The updated template reads customer details from `partner_id` on `stock.quant.package` and prints them on the ZPL label.[file:1][file:3]  
- You can adapt this template to control exactly which customer fields are printed (for example name, street, city, phone, VAT number, etc.).[file:1]  

This lets warehouse staff or carriers quickly identify the destination customer by simply scanning or reading the label.[file:1][file:3]

---

## Requirements

- **Odoo version:** 17.0.[file:1]  
- **Dependencies:**[file:1]  
  - `stock`  
  - `delivery`  

Make sure these core modules are installed and active before installing this module.[file:1]

---

## Installation

1. Copy the module folder (for example `package_label_with_customer/`) into your Odoo `addons` path.[file:1]  
2. Restart the Odoo server so it can detect the new module.  
3. Log in to Odoo as an administrator.  
4. Activate **Developer mode** (Settings → Developer mode).  
5. Go to **Apps**.  
6. Clear the default “Apps” filter if needed, so that all modules are listed.  
7. Search for **Package Label with Customer**.  
8. Click **Install**.[file:1]  

After installation, the new fields will be available on `stock.quant.package` and the updated label report will be ready to use.[file:1][file:3]

---

## Configuration

Depending on your existing setup, you may want to review or adjust the following:

- **Report action used for package labels**  
  - Make sure that the printing action or menu item you use for package labels is linked to the updated ZPL report defined by this module (see `package_label_report.xml`).[file:1]  

- **Printer configuration**  
  - Confirm that your Zebra (or compatible) label printer supports ZPL and is correctly configured in Odoo or via your print server.  
  - Adjust label size, darkness, or orientation in the ZPL template if needed for your labels.[file:1]  

- **Views (optional)**  
  - If you want users to see `picking_id` and `partner_id` on the package form/tree views, you can inherit the relevant views and add these fields in your own XML (this module focuses on adding fields and updating the report template).[file:1][file:3]  

---

## Usage

A typical workflow for this module is:

1. Create or validate a delivery order in Odoo that generates packages (`stock.quant.package`) via picking operations.  
2. For each package, Odoo will create or update move lines that reference this package.  
3. The compute method `_compute_partner_id` runs and:  
   - Finds the latest related move line.  
   - Sets `picking_id` to the corresponding transfer.  
   - Sets `partner_id` to the customer of that transfer.[file:3]  
4. When you print the package label using the configured ZPL report, the label will now include customer details derived from `partner_id`.[file:1][file:3]  

From a user perspective, there is no extra manual step required: everything is computed automatically and reflected in the printed label.[file:3]

---

## Customization and extension

You can safely adapt this module to better match your business rules.

### Adjusting the compute logic

In `stock_quant_package.py`, you can modify `_compute_partner_id` if your process for linking packages to pickings is different:[file:3]

- Change the search domain on `stock.move.line` (for example, ignore certain move types or operations).  
- Change the ordering if you want to prioritize something other than the latest `create_date`.  
- Add extra logic (for example, fallback behavior if multiple pickings are found).  

Always keep this method efficient because it may run on many packages at once.[file:3]

### Changing what appears on the label

In `views/package_label_report.xml`, you can:[file:1]

- Add or remove customer fields (e.g. only show name, or include address and phone).  
- Adjust text size, position, and formatting in the ZPL commands to fit your label dimensions.  
- Add barcodes or QR codes that encode the package ID, picking ID, or customer reference.  

This is the main place where you “design” how the final label will look.[file:1]

### Making fields editable (advanced)

By default, the new fields are computed via `_compute_partner_id` and intended to remain read‑only.[file:3]

If you really need manual override:

- You can change the field definitions to `compute_sudo=True` or add `store=True` depending on your performance and override needs.  
- You can add an inverse or make them editable in views, but keep in mind that this breaks the automatic sync with move lines and pickings unless you implement custom logic.[file:3]  

---

## Troubleshooting

- **Customer does not show on the label**  
  - Check that the package is actually used in at least one `stock.move.line` with a valid `picking_id` and `partner_id`.[file:3]  
  - Verify that the updated ZPL report template is the one being used by your print action.[file:1]  

- **Wrong picking/customer is shown**  
  - Remember that the module uses the *latest* move line (ordered by `create_date`) to determine the picking.[file:3]  
  - If your flow reuses packages across multiple transfers, you may need to adjust `_compute_partner_id` to better match your rules.[file:3]  

- **Nothing printed or printer error**  
  - Test the report in PDF/HTML first in Odoo to verify the content.  
  - Check the ZPL syntax in `package_label_report.xml` for typos after customization.[file:1]  

---

## Module metadata

- Name: `Package Label with Customer`.[file:1]  
- Version: `17.0.1.0.0`.[file:1]  
- Category: `Inventory`.[file:1]  
- Summary: `Customer details in ZPL label on Odoo`.[file:1]  
- Author: `co-ux99`.[file:1]  
- Website: `https://www.illusioweb.com`.[file:1]  
- License: `LGPL-3`.[file:1]  

---

## License

This module is distributed under the **LGPL-3** license, in line with the Odoo Community ecosystem.[file:1][web:8]  
Please refer to the `LICENSE` file in this repository for the full license text.[file:1]
