package br.com.apaschoalon.mapper.custom;

import java.util.Date;

import org.springframework.stereotype.Service;

import br.com.apaschoalon.data.vo.v2.PersonVOV2;
import br.com.apaschoalon.model.Person;


@Service
public class PersonMapper {

	public PersonVOV2 convertEntityToVoV2(Person person) {
		PersonVOV2 vo = new PersonVOV2();

		vo.setAddress(person.getAddress());
		vo.setBirthday(new Date());
		vo.setFirstName(person.getFirstName());
		vo.setGender(person.getGender());
		vo.setId(person.getId());
		vo.setLastName(person.getLastName());
				
		return vo;
	}
	
	public Person convertVOV2ToEntity(PersonVOV2 person) {
		Person entity  = new Person();

		entity .setAddress(person.getAddress());
		// vo.setBirthday(new Date());
		entity .setFirstName(person.getFirstName());
		entity .setGender(person.getGender());
		entity .setId(person.getId());
		entity .setLastName(person.getLastName());
				
		return entity;
	}	

}
