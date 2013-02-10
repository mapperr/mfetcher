package net.mapperr.mangafetcher.modules;

import java.io.File;
import java.util.List;

public class Mangahere
{
	private final String baseUrl = "mangahere.com/";
	
	private String name;
	private List<String> urls;
	
	public File fetchChapter(String volume, String chapter)
	{
		
		return null;
	}
	
	public String getName()
	{
		return name;
	}
	
	public void setName(String name)
	{
		this.name = name;
	}
	
	public List<String> getUrls()
	{
		return urls;
	}
	
	public void setUrls(List<String> urls)
	{
		this.urls = urls;
	}
	
	public String getBaseUrl()
	{
		return baseUrl;
	}
}
