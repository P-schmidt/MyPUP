# https://www.google.com/maps/dir/Prinsengracht+219A,+1015+DT+Amsterdam/Amstelvlietstraat+330,+Amsterdam,+Netherlands/Kolenkitbuurt,+Amsterdam/@52.3618908,4.8383503,13z voorbeeld link


def create_url(list_of_addresses):

    clean_addresses = []
    for address in list_of_addresses:
        address = address.replace(' NL', '')
        address = address.replace('t/m ', '')
        address = address.replace(',', '')
        address = address.replace(' ', '+')
        clean_addresses.append(address)

    url = "https://www.google.com/maps/dir/"
    extra_url = "https://www.google.com/maps/dir/"
    for i, address in enumerate(clean_addresses):
        if i < 10:
            url += address+'/'
            clean_addresses.remove(address)
        else:
            extra_url += address+'/'
            clean_addresses.remove(address)
    if extra_url != "https://www.google.com/maps/dir/":
        return url, extra_url
    else:
        return url