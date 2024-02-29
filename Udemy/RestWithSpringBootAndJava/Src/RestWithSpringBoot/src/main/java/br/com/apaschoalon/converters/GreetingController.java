package br.com.apaschoalon.converters;

import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.apaschoalon.controllers.Greeting;

@RestController
public class GreetingController {


	private static final String template = "Hello, %s!";
	private final AtomicLong  counter = new AtomicLong();
	
	@RequestMapping("/greeting")
	public Greeting greeting(
			@RequestParam(value = "name", defaultValue = "World") 
			String name) {
		return new Greeting(this.counter.incrementAndGet(), String.format(this.template, name));
	}

}
