from convert import ConvertPDF2img


con = ConvertPDF2img()
data = con.pdf2img("../data/test/file_test.pdf")

print(data)